import torch
import json
from typing import Optional, Dict, Any
from monolithic_brain import NeuralSymbolicBrain
import config


class CortexBrainAPI:
    """
    High-level API for Game Engines (Unity, Unreal, Godot, Python Games).
    Abstracts away the complex tensor operations and returns clean structured data.
    """

    def __init__(
        self,
        brain_path: str = config.BRAIN_FILENAME,
        model_path: str = config.MODEL_FILENAME,
    ):
        self.brain_path = brain_path
        self.model_path = model_path
        self.brain: Optional[NeuralSymbolicBrain] = None
        self.loaded = False

    def load(self) -> bool:
        """Loads the brain and body models."""
        print(f"[CortexAPI] Loading Brain from {self.brain_path}...")
        try:
            self.brain = NeuralSymbolicBrain.load_brain(
                self.brain_path, model_path=self.model_path, n_ctx=config.CTX_SIZE
            )
            self.loaded = True
            print("[CortexAPI] Brain Loaded Successfully.")
            if hasattr(self.brain, "system_prompt"):
                print(f"[CortexAPI] Persona: {self.brain.system_prompt}")
            return True
        except Exception as e:
            print(f"[CortexAPI] Error loading brain: {e}")
            return False

    def think(
        self, player_input: str, game_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main cognitive step.
        Args:
            player_input (str): What the player said or did.
            game_context (dict, optional): Current game state (e.g. {"location": "tavern", "health": 100})

        Returns:
            dict: {
                "speech": str,    # What the NPC says
                "action": str,    # Suggested animation/behavior tag
                "uncertainty": float,
                "is_curious": bool,
                "error": str (optional)
            }
        """
        if not self.loaded or not self.brain:
            return {"error": "Brain not loaded"}

        # Construct Contextual Prompt
        prompt = player_input
        if game_context:
            context_str = json.dumps(game_context, ensure_ascii=False)
            prompt = f"[Context: {context_str}] {player_input}"

        # Forward Pass
        try:
            with torch.no_grad():
                results = self.brain(prompt, max_tokens=128)

            # Parse Results
            speech = results["text"].strip()
            uncertainty = results["uncertainty"]

            # Simple heuristic
            action = "IDLE"
            if "fighting" in speech.lower() or "attack" in speech.lower():
                action = "COMBAT_STANCE"
            elif "?" in speech:
                action = "THINKING"

            return {
                "speech": speech,
                "action": action,
                "uncertainty": float(uncertainty),
                "is_curious": bool(results["needs_reflection"]),
            }
        except Exception as e:
            print(f"[CortexAPI] Error during think: {e}")
            return {"speech": "...", "action": "ERROR", "error": str(e)}

    def save(self):
        """AUTO-SAVE the brain (memories/adaptation)."""
        if self.loaded and self.brain:
            self.brain.save_brain(self.brain_path)
            print("[CortexAPI] Brain verified and saved.")
