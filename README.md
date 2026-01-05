# Cortex Module

**Autonomous AI for Game NPCs: Unifying LLM, HDC, and Active Inference.**

このプロジェクトは、ゲームのNPC（Non-Player Character）に搭載可能な、**優秀な自律AIモジュール「Cortex Module」** を開発するものです。
単一のファイル（`.brain`）として持ち運び可能で、以下の特徴を持ちます：
- **軽量**: GGUFモデルと連携し、ローカル環境で高速動作。
- **記憶**: HDCにより、プレイヤーとの対話やゲーム内イベントを長期記憶。
- **自律**: 能動的推論により、自ら考え、行動を選択する。

## 🧠 Core Architecture

この脳は3つの主要なレイヤーで構成されています：

1.  **Cortex (大脳皮質)**: `Transformer` (LLM)
    *   外部情報の処理、思考の生成、言語能力を担当します。
2.  **Hippocampus (海馬)**: `HDC (Hyperdimensional Computing)`
    *   ニューラルな隠れ状態を固定長の超次元ベクトルに射影し、シンボルとして操作・記憶します。
3.  **Prefrontal Cortex (前頭葉)**: `Active Inference Controller`
    *   自身の予測のエントロピー（不確実性）を監視し、「探索（思考）」するか「活用（行動）」するかを決定します。

## 📦 Installation

必要要件: Python 3.10+, Windows 10/11
詳細なセットアップ手順は [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) を参照してください。

```powershell
# 1. llama-cpp-python (CPU Stable)
pip install https://github.com/abetlen/llama-cpp-python/releases/download/v0.2.90/llama_cpp_python-0.2.90-cp310-cp310-win_amd64.whl

# 2. Dependencies
pip install torch numpy
```

## 🚀 Quick Start

### 1. Forge the Brain (脳の鋳造 & 人格設定)
ベースモデルをダウンロードし、**人格 (Persona)** とHDC行列を初期化します。

```powershell
python src/forge_brain.py
```
*   `1. English Knight`, `2. Japanese Samurai`, `3. Custom` から人格を選択できます。
*   -> `my_agent.brain` (Soul) と `qwen2.5...gguf` (Body) が準備されます。

### 2. Awaken (覚醒 & テスト)
単体テスト用のスクリプトで対話を試します。

```powershell
python src/awaken_brain.py
```

### 3. Game Integration (ゲームへの組み込み)
`CortexBrainAPI` を使用して、あなたのゲームからAIを呼び出します。

```python
from src.cortex_api import CortexBrainAPI

brain = CortexBrainAPI()
brain.load()
response = brain.think("こんにちは", game_context={"location": "Town"})
print(f"NPC: {response['speech']}")
```

## 📂 Project Structure

- `src/monolithic_brain.py`: **Core Logic**. Dual-Llama構成、HDC記憶、意図制御。
- `src/forge_brain.py`: セットアップスクリプト。人格設定機能付き。
- `src/awaken_brain.py`: 動作確認用CLI。
- `src/cortex_api.py`: **Game Engine API**. 外部利用はここから。
- `src/test_game_integration.py`: ゲームループのシミュレーション。
- `src/verify_memory.py`: 記憶機能の検証スクリプト。
- `docs/ARCHITECTURE.md`: アーキテクチャ設計書。
- `docs/DEVELOPMENT.md`: 開発環境セットアップガイド。
