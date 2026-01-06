# 🧠 Project Cortex

> **"Inject a Cortex into your NPCs."**
> 
> あなたのNPCに、脳を注入しよう。

[🇺🇸 English README](README.md)

---

**Lightweight** — メモリ1GBで動作する極小の脳  
**Persistent** — 会話を「地層」のように記憶し、決して忘れない  
**Autonomous** — ただ答えるだけでなく、自ら考え、悩み、行動する

---

## ✨ What is Cortex?

CortexはゲームNPCに**記憶**と**感情**を与える、スタンドアロンAIエンジンです。

| Feature | Description |
|---------|-------------|
| 🗣️ **Natural Dialogue** | LLM (Qwen2.5-1.5B) による自然な会話 |
| 🧠 **Memory (HDC)** | 過去の会話を記憶し、関連する話題で想起 |
| 😊 **Emotion** | 思考の確信度から感情を検出 (`confident`, `neutral`, `uncertain`, `confused`) |
| 📦 **Standalone** | Python不要、`Cortex.exe` 単体で動作 |

---

## 📦 Distribution Package

```
CortexAI/
├── Cortex.exe           # 思考エンジン本体（これを起動するだけ）
├── persona.txt          # NPC性格設定（編集してカスタマイズ！）
├── models/
│   └── qwen-1.5b.gguf   # 脳の実体
├── memories/            # HDC記憶データが蓄積される場所
│   ├── Villager_A.mem   # 村人Aの記憶
│   └── Lydia.mem        # リディアの記憶
└── examples/
    ├── Minecraft_Mod/   # Minecraftサンプルコード
    └── Skyrim_Mod/      # Skyrimサンプルコード
```

> ⚠️ **重要:** `Program Files` などの書き込み禁止フォルダには展開しないでください。Modフォルダやデスクトップに展開してご使用ください。

---

## 🚀 Quick Start

### 1. Run the Cortex
```bash
Cortex.exe
# Server running on http://127.0.0.1:8000
```

### 2. Connect Your NPC
```python
import requests

response = requests.post("http://127.0.0.1:8000/chat", json={
    "text": "こんにちは、自己紹介して",
    "speaker": "Player"
})

npc_reply = response.json()
print(f"NPC: {npc_reply['reply']}")
print(f"Emotion: {npc_reply['emotion']}")
# NPC: 私は賢明な哲学者であり...
# Emotion: confident
```

---

## 📡 API Reference

### POST `/chat`
Main conversation endpoint.

**Request:**
```json
{
  "text": "プレイヤーの発言",
  "speaker": "Player"
}
```

**Response:**
```json
{
  "reply": "NPCの応答",
  "emotion": "confident | neutral | uncertain | confused",
  "resonance": 0-100,
  "memories_recalled": [{"text": "過去の発言", "similarity": 0.85}]
}
```

### POST `/inject`
Inject game context without dialogue.

```json
{
  "info": {"location": "Castle", "time": "night", "weather": "rain"}
}
```

### POST `/forget`
Reset all memories and conversation history.

---

## 🧠 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Project Cortex                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐    ┌─────────────┐    ┌──────────┐   │
│   │   Cortex    │───▶│ Hippocampus │───▶│  Memory  │   │
│   │    (LLM)    │    │    (HDC)    │    │  (JSON)  │   │
│   └─────────────┘    └─────────────┘    └──────────┘   │
│         │                                     ▲         │
│         ▼                                     │         │
│   ┌─────────────┐                             │         │
│   │  Emotion    │─────────────────────────────┘         │
│   │  (Entropy)  │                                       │
│   └─────────────┘                                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Cortex (大脳皮質)** — Transformer LLM が思考を生成  
**Hippocampus (海馬)** — 思考を4096次元ベクトルに投影、類似検索  
**Memory (地層記憶)** — 会話が蓄積され、永続化

---

## 🏗️ Build from Source

### Requirements
- Python 3.10+
- llama-cpp-python

### Install
```bash
pip install llama-cpp-python fastapi uvicorn numpy
```

### Run Development Server
```bash
python src/server.py
```

### Build Executable
```bash
.\build_cortex.bat
# Output: dist/CortexAI/
```

---

## 🎮 Integration Examples

### Minecraft (Lua)
```lua
local http = require("http")
local response = http.post("http://127.0.0.1:8000/chat", {
    text = "What should I do today?",
    speaker = "Steve"
})
npc:say(response.reply)
```

### Skyrim (Papyrus)
```papyrus
; Call Cortex API via SKSE HTTP plugin
String response = CortexAPI.Chat("Hello traveler!", "Player")
Debug.Notification(response)
```

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [Qwen2.5](https://github.com/QwenLM/Qwen2.5)
- Hyperdimensional Computing concept

---

> *"Give your NPCs a brain, not just a script."*
