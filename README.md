# 🧠 Project Cortex

> **"Inject a Cortex into your NPCs."**
> 
> Give your game characters a brain, not just a script.

[🇯🇵 日本語版 README](README_ja.md)

---

**Lightweight** — Runs on just 1GB of RAM  
**Persistent** — Remembers conversations like geological layers, never forgets  
**Autonomous** — Doesn't just answer, thinks, hesitates, and acts on its own

---

## ✨ What is Cortex?

Cortex is a standalone AI engine that gives your game NPCs **memory** and **emotion**.

| Feature | Description |
|---------|-------------|
| 🗣️ **Natural Dialogue** | Powered by LLM (Qwen2.5-1.5B) |
| 🧠 **Memory (HDC)** | Remembers past conversations and recalls relevant topics |
| 😊 **Emotion** | Detects emotion from thought certainty (`confident`, `neutral`, `uncertain`, `confused`) |
| 📦 **Standalone** | No Python required, just run `Cortex.exe` |

---

## 📦 Distribution Package

```
CortexAI/
├── Cortex.exe           # The brain engine (just run this)
├── persona.txt          # NPC personality (edit to customize!)
├── models/
│   └── qwen-1.5b.gguf   # The brain itself
├── memories/            # Where HDC memory data accumulates
│   ├── Villager_A.mem   # Villager A's memories
│   └── Lydia.mem        # Lydia's memories
└── examples/
    ├── Minecraft_Mod/   # Sample code for Minecraft
    └── Skyrim_Mod/      # Sample code for Skyrim
```

> ⚠️ **Important:** Do NOT extract to `Program Files` or other write-protected locations. Extract to your Mod folder or Desktop for proper operation.

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
    "text": "Hello, introduce yourself!",
    "speaker": "Player"
})

npc_reply = response.json()
print(f"NPC: {npc_reply['reply']}")
print(f"Emotion: {npc_reply['emotion']}")
# NPC: I am a wise philosopher and your loyal companion...
# Emotion: confident
```

---

## 📡 API Reference

### POST `/chat`
Main conversation endpoint.

**Request:**
```json
{
  "text": "Player's message",
  "speaker": "Player"
}
```

**Response:**
```json
{
  "reply": "NPC's response",
  "emotion": "confident | neutral | uncertain | confused",
  "resonance": 0-100,
  "memories_recalled": [{"text": "Past message", "similarity": 0.85}]
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

**Cortex (Cerebral Cortex)** — Transformer LLM generates thoughts  
**Hippocampus** — Projects thoughts into 4096-dim vectors, similarity search  
**Memory (Geological Memory)** — Conversations accumulate and persist

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

See the `examples/` folder for complete integration code:

- **[Minecraft (Lua)](examples/Minecraft_Mod/)** — ComputerCraft integration
- **[Skyrim (Papyrus)](examples/Skyrim_Mod/)** — SKSE script examples

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [Qwen2.5](https://github.com/QwenLM/Qwen2.5)
- Hyperdimensional Computing research

---

> *"Give your NPCs a brain, not just a script."*
