import numpy as np
import torch
from llama_cpp import Llama
from typing import Generator, Tuple, List, Dict, Any, Optional
import config

class MonolithicCortex:
    """
    Low-level Monolithic Brain implementation using manual eval loop.
    Unifies Language (Left) and Meaning (Right) hemispheres into a single stream.
    """
    def __init__(
        self, 
        model_path: str = config.MODEL_FILENAME,
        system_prompt: str = config.DEFAULT_PERSONA,
        n_ctx: int = config.CTX_SIZE,
        n_gpu_layers: int = 0
    ):
        """
        Initialize Llama with embedding=True to enable the 'Right Hemisphere'.
        """
        print(f"[MonolithicCortex] Loading Model from {model_path}...")
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            embedding=False, # Disabled to fix crash. Vectors will be zeros for now.
            logits_all=True, # Re-enabled for Active Inference
            verbose=False
        )
        self.system_prompt = system_prompt
        
        # Cache management (Simple sliding window later, for now relying on Llama's smart context)
        # self.cache = LlamaRamCache(capacity_bytes=...) 
        
        print(f"[MonolithicCortex] Initialized. Persona: {system_prompt[:30]}...")

    def calculate_entropy(self, logits: np.ndarray, top_k: int = 40) -> float:
        """
        Calculates Shannon entropy of the next token distribution with Top-K filtering.
        Used for Active Inference (Metacognition).
        """
        # 1. Softmax & Top-K
        # Explicitly copy to avoid side effects if strictly needed, but here simple ops are fine
        
        # Get indices of top_k values
        if top_k > 0 and top_k < len(logits):
            top_k_indices = np.argpartition(logits, -top_k)[-top_k:]
            top_k_logits = logits[top_k_indices]
            # We don't need accurate global probs, just local uncertainty shape
            logits = top_k_logits
            
        # Stable Softmax
        # Subtract max for stability
        logits = logits - np.max(logits)
        exp_logits = np.exp(logits)
        probs = exp_logits / np.sum(exp_logits)
        
        # 3. Entropy calc: -sum(p * log(p))
        entropy = -np.sum(probs * np.log(probs + 1e-10))
        return float(entropy)

    def think_stream(
        self, 
        user_input: str, 
        game_context: Optional[Dict[str, Any]] = None,
        max_tokens: int = 128,
        temperature: float = 0.7,
        stop_tokens: List[str] = ["User:", "System:", "\n\n"]
    ) -> Generator[Tuple[str, np.ndarray, float], None, None]:
        """
        Generator that yields (token, vector, entropy) at every step.
        """
        # 1. Construct Prompt
        #    [System] + [Status] + [User]
        context_str = self._format_context(game_context)
        
        # ChatML-ish or Simple format
        full_prompt = f"System: {self.system_prompt}\n{context_str}\nUser: {user_input}\nAssistant:"
        
        # 2. Tokenize & Prefill (eval full prompt)
        tokens = self.llm.tokenize(full_prompt.encode("utf-8"))
        print(f"[DEBUG] Full Prompt: {full_prompt[:50]}...")
        print(f"[DEBUG] Token Count: {len(tokens)}")
        print(f"[DEBUG] Tokens: {tokens[:10]}...")
        
        if not tokens:
            print("[DEBUG] No tokens to eval!")
            return

        # Prefill
        try:
            self.llm.eval(tokens)
        except Exception as e:
            print(f"[DEBUG] CRASH during prefill eval: {e}")
            raise e
        
        # 3. Generation Loop
        
        # Track generated tokens to handle stop sequences manually if needed (or simply check current string)
        generated_text = ""
        
        for _ in range(max_tokens):
            # A. Get Logits & Embedding from cache (Result of previous eval)
            # logits() returns logits for the LAST token evaluated
            logits = np.array(self.llm.logits())
            logits = logits[-1, :] if logits.ndim > 1 else logits # Handle batch dim if present
            
            # embeddings() returns embedding for the LAST token evaluated
            if self.llm.context_params.embedding:
                embedding = np.array(self.llm.embeddings())
                # embedding might be list of lists if batch > 1
                if embedding.ndim > 1:
                     embedding = embedding[-1]
            else:
                embedding = np.zeros(1536) # Fallback (should not happen if init correct)

            # B. Calc Entropy (Active Inference)
            entropy = self.calculate_entropy(logits)
            
            # C. Sample Next Token
            # sample() expects logits
            next_token_id = self.llm.sample(
                logits, 
                temperature=temperature,
                top_p=0.9
            )
            
            # D. Decode
            token_str = self.llm.detokenize([next_token_id]).decode("utf-8", errors="ignore")
            generated_text += token_str
            
            # E. Yield Result (Synchronous Thought & Speech)
            yield token_str, embedding, entropy
            
            # F. Check Stop Conditions
            if next_token_id == self.llm.token_eos():
                break
            
            stop_hit = False
            for s in stop_tokens:
                if s in generated_text: # Simple check, might need strict suffix check
                    # If we generated a stop token, we break. 
                    # Refinement: Check if the *newly added* text completes a stop seq.
                    # For simple "User:", this is fine.
                    stop_hit = True
                    break
            if stop_hit:
                break

            # G. Update Cache (eval next token)
            self.llm.eval([next_token_id])

    def _format_context(self, context: Optional[Dict[str, Any]]) -> str:
        """Helper to format dictionary into [Status: ...] string"""
        if not context:
            return ""
        # Simple Key-Value dump
        s = ", ".join([f"{k}={v}" for k, v in context.items()])
        return f"[System: Status={{{s}}}]"
