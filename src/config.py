"""
Cortex Module Configuration
Central source of truth for file paths, dimensions, and model settings.
"""

# Model Files
MODEL_URL = "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"
MODEL_FILENAME = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
BRAIN_FILENAME = "my_agent.brain"

# Core Dimensions
HDC_DIM = 4096  # Hyperdimensional Vector Size
EMBED_DIM_DETECT = 1536  # Default fallback embedding size for Qwen2.5-1.5B
CTX_SIZE = 4096  # Context Window

# Active Inference
CURIOSITY_THRESHOLD = 2.5
ENERGY_BUDGET = 100.0

# System Defaults
DEFAULT_PERSONA = "You are a helpful AI assistant."
