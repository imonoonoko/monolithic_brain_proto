# 🧠 CortexAI Initial Release (beta)

> **"Inject a Cortex into your NPCs."**
> 
> Give your game characters a brain, not just a script.

Initial public release of Project Cortex, a standalone AI engine designed for Game Modders.

## ✨ Key Features

- **🗣️ Natural Dialogue**: Powered by a lightweight 1.5B LLM (Qwen2.5), running locally on CPU/GPU.
- **🧠 Geological Memory (HDC)**: NPCs remember past conversations and context using Hyperdimensional Computing.
- **😊 Emotion System**: Automatically detects NPC confidence and emotional state (`confident`, `neutral`, `uncertain`, `confused`) based on entropy.
- **📦 Mod-Ready**: simple HTTP API (`/chat`, `/inject`) with examples for **Minecraft (Lua)** and **Skyrim (Papyrus)**.

## 📦 What's Included

- `Cortex.exe`: The standalone engine.
- `setup_models.bat`: **Run this first!** Downloads the AI model (1GB).
- [persona.txt](persona.txt): Editable text file to customize your NPC's personality.
- `examples/`: Integration code for Minecraft and Skyrim.

## 🚀 Quick Start

1. Extract the zip to your Mod folder (DO NOT put in Program Files).
2. **Run `setup_models.bat`** to download the brain.
3. Run `Cortex.exe`.
4. Send a POST request to `http://127.0.0.1:8000/chat`.

## ⚠️ Notes

- This is a v0.1 Beta release.
- Ensure you have write permissions in the extraction folder for memory saving to work.
- Customize [persona.txt](persona.txt) to change the AI's character!

---

*Happy Modding!* 🎮
