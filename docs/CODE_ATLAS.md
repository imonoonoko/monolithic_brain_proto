# Code Atlas: Cortex Module

## Source Code (`src/`)

### `config.py`
Central configuration for all modules.
- **Constants**: `MODEL_FILENAME`, `HDC_DIM` (4096), `EMBED_DIM` (1536).
- **Paths**: GGUF Model URL, Brain persistence path.

### `monolithic_brain.py`
Core neural-symbolic implementation.
- **Class `NeuralSymbolicBrain`**:
    - Dual-Llama management (Left/Right hemispheres).
    - `forward()`: Generation -> Embedding -> HDC Projection -> Memory Storage.
- **Class `HDCProjection`**:
    - Random projection matrix buffer.
    - Projects `(1, 1536)` -> `(1, 4096)` Bipolar Tensor.
- **Class `EpisodicMemory`**:
    - Superposition storage.
    - `recall_memory()`: Cosine similarity check.

### `cortex_api.py`
High-level interface for external applications.
- **Class `CortexBrainAPI`**:
    - `load()`: Initializes backend with config.
    - `think()`: Simple Input -> Output map.
    - `save()`: Persists state.

### `forge_brain.py`
Setup utility.
- Downloads GGUF model.
- Initializes random matrices.
- Injects System Prompt (Persona).

### `awaken_brain.py`
CLI Verification tool.
- Uses `CortexBrainAPI` to run a conversational test loop.

### `test_game_integration.py`
Simulation script.
- Simulates a game loop with changing inputs/context to verify API latency and state.

### `verify_memory.py`
Unit test for Memory subsystem.
- Manually injects vectors to test superposition recall rates.
