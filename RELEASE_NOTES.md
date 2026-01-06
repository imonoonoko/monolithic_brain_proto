# 🧠 CortexAI Initial Release (beta)

> **"Inject a Cortex into your NPCs."** / **"NPCに、スクリプトではなく脳を与えよう"**

CortexAI (Project Cortex) は、ゲームModder向けに設計されたスタンドアロンのAIエンジンです。

---

## ✨ Features (主な機能)

- **🗣️ Natural Dialogue (自然な対話)**:
    - Powered by Qwen2.5-1.5B (Lightweight LLM). Runs locally on CPU/GPU.
    - 軽量LLM (Qwen2.5) を搭載。CPU/GPUでローカル動作します。

- **🧠 Geological Memory (地質学的記憶)**:
    - Uses Hyperdimensional Computing (HDC) to remember conversations like geological layers.
    - 超次元計算 (HDC) を用いて、会話や文脈を地層のように記憶・想起します。

- **😊 Emotion System (感情システム)**:
    - Automatically detects confidence (`confident`, `uncertain`, etc.) based on entropy.
    - 思考のエントロピーから、「自信あり」「混乱」などの感情状態を自動検出します。

- **📦 Mod-Ready (Mod親和性)**:
    - Simple HTTP API (`/chat`). Integration examples included for **Minecraft (Lua)** & **Skyrim (Papyrus)**.
    - シンプルなHTTP API。マイクラ(Lua)やスカイリム(Papyrus)の連携サンプルも同梱。

---

## 📦 What's Included (同梱物)

- `Cortex.exe`: The AI Engine. / AIエンジン本体。
- `setup_models.bat`: **Run FIRST!** Downloads the AI model (1GB). / **最初に実行してください！** AIモデルをダウンロードします。
- `persona.txt`: Customize NPC personality here. / NPCの性格を自由に設定できるファイル。
- `examples/`: API integration code. / 連携用サンプルコード。

---

## 🚀 Quick Start (使い方)

1. **Extract** the zip. (⚠️ DO NOT use `Program Files`. Use Desktop or Mod folder.)
   - Zipを解凍します (※書き込み権限のある場所に置いてください)。

2. **Run `setup_models.bat`**. (Downloads the brain)
   - `setup_models.bat` を実行して、AIモデルをダウンロードします。

3. **Run `Cortex.exe`**.
   - `Cortex.exe` を起動します。

4. Send **POST request** to `http://127.0.0.1:8000/chat`.
   - APIにリクエストを送って会話開始！

---

## ⚠️ Notes (注意)

- **Beta Release (v0.1)**: Experimental build.
- **Permissions**: Requires write permission for `memories/` folder.
  - `memories/` フォルダに記憶を保存するため、書き込み権限が必要です。
- **Customization**: Edit `persona.txt` to change the character!
  - `persona.txt` を書き換えて、あなただけのキャラを作ってください！

---
*Happy Modding!* 🎮
