import torch
import torch.nn as nn
import numpy as np
from typing import List, Union, Tuple, Dict, Any
from llama_cpp import Llama
import config


class HDCProjection(nn.Module):
    """
    Projects the LLM's embedding (from llama.cpp) into a fixed high-dimensional space.
    """

    def __init__(self, input_dim: int, hdc_dim: int = config.HDC_DIM):
        super().__init__()
        # Fixed random projection matrix (Gaussian random projection)
        # Registered as buffer to save with state_dict
        self.register_buffer("projection_matrix", torch.randn(input_dim, hdc_dim))
        self.input_dim = input_dim
        self.hdc_dim = hdc_dim

    def forward(self, embedding_list: Union[List[float], torch.Tensor]) -> torch.Tensor:
        """
        Args:
            embedding_list: List[float] or Tensor
        Returns:
            hdc_vector: (1, hdc_dim) Bipolar Tensor
        """
        # Handle Input
        if isinstance(embedding_list, torch.Tensor):
            x = embedding_list
        else:
            x = torch.tensor(embedding_list, dtype=torch.float32)

        if x.dim() == 1:
            x = x.unsqueeze(0)  # (1, input_dim)

        # Projection: X * W
        projected = torch.matmul(x, self.projection_matrix)
        return torch.sign(projected)  # Bipolar HDC (-1, 1)


class ActiveInferenceController(nn.Module):
    """
    Control logic based on prediction entropy.
    """

    def __init__(self):
        super().__init__()
        self.register_buffer(
            "curiosity_threshold", torch.tensor(config.CURIOSITY_THRESHOLD)
        )
        self.register_buffer("energy_budget", torch.tensor(config.ENERGY_BUDGET))

    def forward(self, logits_np: np.ndarray) -> Tuple[bool, float]:
        """
        Args:
            logits_np: numpy array of shape (n_tokens, vocab_size) or (1, vocab_size)
        """
        # Convert to torch for easy entropy calc
        logits = torch.tensor(logits_np, dtype=torch.float32)
        if logits.dim() == 1:
            logits = logits.unsqueeze(0)

        # Calculate Entropy
        probs = torch.softmax(logits, dim=-1)
        log_probs = torch.log(probs + 1e-9)
        entropy = -torch.sum(probs * log_probs, dim=-1)  # (1,)

        return entropy.item() > self.curiosity_threshold.item(), entropy.item()


class EpisodicMemory(nn.Module):
    """
    HDC-based Episodic Memory (Hippocampus).
    Stores memories by superposing bipolar vectors.
    """

    def __init__(self, hdc_dim: int = config.HDC_DIM, decay_rate: float = 0.01):
        super().__init__()
        self.hdc_dim = hdc_dim
        self.decay_rate = decay_rate
        # Memory trace is a single float vector (sum of bipolar vectors)
        self.register_buffer("memory_trace", torch.zeros(1, hdc_dim))

    def add_memory(self, hdc_vector: torch.Tensor):
        """
        Encodes an event (hdc_vector) into the memory trace via superposition (addition).
        Args:
            hdc_vector: (1, hdc_dim) Tensor, Bipolar {-1, 1}
        """
        self.memory_trace = self.memory_trace * (1.0 - self.decay_rate)
        self.memory_trace += hdc_vector

    def recall_memory(
        self, query_vector: torch.Tensor, threshold: float = 0.0
    ) -> float:
        """
        Checks if a query vector exists in the superposition via Cosine Similarity.
        Returns:
            similarity: float (-1.0 to 1.0)
        """
        if torch.norm(self.memory_trace) < 1e-9:
            return 0.0

        sim = torch.nn.functional.cosine_similarity(query_vector, self.memory_trace)
        return sim.item()


class NeuralSymbolicBrain(nn.Module):
    """
    Monolithic Brain using llama.cpp backend.
    """

    def __init__(
        self,
        model_path: str = config.MODEL_FILENAME,
        n_ctx: int = config.CTX_SIZE,
        **kwargs,
    ):
        super().__init__()
        print(f"Loading Cortex (GGUF) from {model_path}...")

        # Instance 1: Generation (Left Hemisphere)
        print("  - Initializing Generator (Left Hemisphere)...")
        self.llm_gen = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            embedding=False,
            logits_all=False,
            verbose=False,
            **kwargs,
        )

        # Instance 2: Embedding (Right Hemisphere / Hippocampus Feed)
        print("  - Initializing Embedder (Right Hemisphere)...")
        self.llm_embed = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            embedding=True,
            logits_all=False,
            verbose=False,
            **kwargs,
        )

        # Inspect embedding size
        try:
            dummy_embed = self.llm_embed.create_embedding("Init")["data"][0][
                "embedding"
            ]
            embed_dim = len(dummy_embed)
            if embed_dim < 16:
                print(
                    f"Warning: Detected embedding dimension {embed_dim} looks suspicious. Fallback to {config.EMBED_DIM_DETECT}."
                )
                embed_dim = config.EMBED_DIM_DETECT
        except Exception as e:
            print(
                f"Warning: Could not detect embedding dimension ({e}). Fallback to {config.EMBED_DIM_DETECT}."
            )
            embed_dim = config.EMBED_DIM_DETECT

        print(f"Final Brain Embedding Dimension: {embed_dim}")

        # Components
        self.hippocampus = HDCProjection(embed_dim, hdc_dim=config.HDC_DIM)
        # Memory storage
        self.episodic_memory = EpisodicMemory(hdc_dim=config.HDC_DIM)
        self.pfc = ActiveInferenceController()

    def forward(self, prompt, max_tokens=64):
        """
        Generates text and captures the internal state of the 'thought'.
        Automatically stores the generated thought into episodic memory.
        """
        # Prepend System Prompt if available
        full_prompt = prompt
        if hasattr(self, "system_prompt") and self.system_prompt:
            # Very simple chat formatting for Qwen/Llama-3
            # For a "Monolithic" vibe, we just prepend it.
            # Refined approach: Use proper chat template if model supports it,
            # but here we stick to raw text completion for simplicity/speed.
            # "System: ... \nUser: ... \n"
            full_prompt = f"System: {self.system_prompt}\nUser: {prompt}\nAssistant:"

        # 1. Cortex Processing (Generation) via Left Hemisphere
        response = self.llm_gen.create_completion(
            full_prompt,
            max_tokens=max_tokens,
            echo=False,  # Do NOT echo system prompt in output text
            stop=["User:", "System:"],  # Stop if it tries to hallucinate new turns
        )

        text = response["choices"][0]["text"]

        # 2. Hippocampal Projection via Right Hemisphere
        # We assume the 'thought' state is represented by the embedding of the generated text
        embed_resp = self.llm_embed.create_embedding(text)
        current_embedding = embed_resp["data"][0][
            "embedding"
        ]  # List[float] OR List[List[float]]

        # Robust Mean Pooling
        embed_tensor = torch.tensor(current_embedding, dtype=torch.float32)
        if embed_tensor.dim() == 2:
            # Sequence of embeddings -> Mean Pool to get single thought vector
            embed_tensor = torch.mean(
                embed_tensor, dim=0, keepdim=True
            )  # (1, embed_dim)
        elif embed_tensor.dim() == 1:
            embed_tensor = embed_tensor.unsqueeze(0)  # (1, embed_dim)

        # Pass tensor directly to Hippocampus
        hdc_thought = self.hippocampus(embed_tensor)

        # Store in Episodic Memory (Consolidation)
        self.episodic_memory.add_memory(hdc_thought)

        # 3. Active Inference (Entropy check)
        # Placeholder uncertainty since logprobs are unstable in this version
        uncertainty = 0.0

        needs_reflection = uncertainty > self.pfc.curiosity_threshold.item()

        return {
            "text": text,
            "hdc_thought": hdc_thought,
            "uncertainty": uncertainty,
            "needs_reflection": needs_reflection,
        }

    def save_brain(self, path):
        """Saves learned parameters + Metadata (System Prompt)."""
        # We wrap state_dict in a larger dict
        data = {
            "state_dict": self.state_dict(),
            "config": {
                "system_prompt": getattr(self, "system_prompt", ""),
                "embedding_dim": self.hippocampus.input_dim,
            },
        }
        torch.save(data, path)

    @classmethod
    def load_brain(cls, path, model_path, **kwargs):
        # Load the full package
        data = torch.load(path)

        # If it's the old format (just state_dict), handle gracefully
        if "state_dict" not in data:
            print("Loading legacy brain format...")
            state_dict = data
            config = {}
        else:
            state_dict = data["state_dict"]
            config = data["config"]

        brain = cls(model_path, **kwargs)
        brain.load_state_dict(state_dict)

        # Restore config
        if "system_prompt" in config:
            brain.system_prompt = config["system_prompt"]
            print(f"Restored Persona: {brain.system_prompt[:50]}...")

        return brain
