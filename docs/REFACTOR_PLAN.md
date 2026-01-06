# Refactor Plan: Polymerization 🛡️

## 1. Objectives
- **Centralize Configuration**: Remove scattered magic numbers and file paths.
- **Type Safety**: Add proper type hints to core modules.
- **DRY (Don't Repeat Yourself)**: Eliminate duplicate loading logic by making `awaken_brain.py` use `CortexBrainAPI`.

## 2. Changes

### Step 1: Central Config ⚙️
- **[NEW] `src/config.py`**
    - `MODEL_PATH`: "qwen2.5-1.5b-instruct-q4_k_m.gguf"
    - `BRAIN_PATH`: "my_agent.brain"
    - `HDC_DIM`: 4096
    - `CTX_SIZE`: 4096 (Unified)
    - `EMBED_DIM`: 1536

### Step 2: Core Refactor 🧠
- **[MODIFY] `src/monolithic_brain.py`**
    - Import `config`.
    - Add Type Hints (`torch.Tensor`, `List[float]`).
    - Use `config.HDC_DIM` etc.

### Step 3: API & Forge Update 🛠️
- **[MODIFY] `src/forge_brain.py`**
    - Use `config.MODEL_PATH`.
- **[MODIFY] `src/cortex_api.py`**
    - Add Type Hints.
    - detailed docstrings.

### Step 4: Unification 🔗
- **[Refactor] `src/awaken_brain.py`**
    - **DELETE** existing logic.
    - **REPLACE** with a CLI wrapper around `CortexBrainAPI`.

## 3. Verification
- Run `forge_brain.py` (dry run or check paths).
- Run `awaken_brain.py` (should work same as before but via API).
- Run `test_game_integration.py` (regression test).
