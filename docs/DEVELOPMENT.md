# Development Environment Setup (Windows) 🪟

このプロジェクトは Windows 環境での開発を前提としています。
`llama-cpp-python` を使用して GGUF モデルを動作させるためのセットアップ手順を記述します。

## Prerequisites

- **OS**: Windows 10/11
- **Python**: 3.10 (推奨) or 3.11/3.12
- **Powershell**: ターミナル操作に使用

## Installation Guide

### 1. `llama-cpp-python`

Windows 環境では、コンパイル済みの Wheel を使用しないとインストールに失敗することがあります（Visual Studio Build Tools がない場合）。

#### Stable (CPU Only) - Version 0.2.90
安定して動作確認ができているバージョンです。

```powershell
pip install https://github.com/abetlen/llama-cpp-python/releases/download/v0.2.90/llama_cpp_python-0.2.90-cp310-cp310-win_amd64.whl
```

#### Latest (Possible Issues)
最新版を使いたい場合は、以下のコマンドで CPU 用のビルド済みバイナリを指定します。

```powershell
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```
※ GPU (CUDA) 版を使用する場合は、`whl/cpu` を `whl/cu121` (CUDA 12.1の場合) などに変更してください。

### 2. Dependencies

その他の依存ライブラリをインストールします。

```powershell
pip install torch numpy transformers
```

## Model Setup (GGUF) & Persona

このプロジェクトでは **GGUF形式** の軽量モデルを使用します。
スクリプト `src/forge_brain.py` を実行すると、モデルのダウンロードと初期設定（人格注入）が行われます。

1. **Download**: `src/forge_brain.py` 実行時に自動ダウンロード (Qwen2.5-1.5B)。
2. **Forge (Persona)**: 実行中に対話形式で人格（Prompt）を選択できます。
    - `1. English Knight`
    - `2. Japanese Samurai`
    - `Custom`: 独自プロンプト入力

## API Integration (For Developers)

ゲームエンジンや外部アプリから脳を利用する場合は、`src/cortex_api.py` を使用します。

```python
from src.cortex_api import CortexBrainAPI

# Load the brain
brain = CortexBrainAPI(brain_path="my_agent.brain")
brain.load()

# Interaction Loop
response = brain.think("Hello", game_context={"hp": 100})
# response -> {'speech': '...', 'action': 'IDLE', ...}
```

## Troubleshooting

- **ImportError: DLL load failed**: `llama-cpp-python` のバージョンが Python のバージョンと一致していない可能性があります。`cp310` (Python 3.10) など、環境に合った Wheel を使用してください。
- **Build Error**: `pip install llama-cpp-python` を直接実行すると、C++ コンパイラを探しに行って失敗します。必ず Wheel URL または `--extra-index-url` を指定してください。
