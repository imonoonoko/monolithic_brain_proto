# Cortex NPC Integration for Skyrim

[🇯🇵 日本語版](README_ja.md)

This folder contains example Papyrus scripts for integrating Project Cortex with Skyrim Special Edition.

## Requirements

- **Cortex.exe** running on the same machine (port 8000)
- **SKSE64** (Skyrim Script Extender)
- HTTP plugin for Papyrus (one of the following):
  - [PapyrusHTTP](https://www.nexusmods.com/skyrimspecialedition/mods/)
  - [JContainers](https://www.nexusmods.com/skyrimspecialedition/mods/16495) with HTTP support

## Files

| File | Description |
|------|-------------|
| `CortexAPI.psc` | Core API wrapper for HTTP communication |
| `CortexNPC.psc` | Example NPC script with full integration |

## Setup

1. **Start Cortex:**
   ```bash
   Cortex.exe
   ```

2. **Install Scripts:**
   - Copy `.psc` files to `Data/Scripts/Source/`
   - Compile with Creation Kit or Papyrus Compiler

3. **Attach to NPC:**
   - In Creation Kit, attach `CortexNPC` script to your NPC
   - Set `NPCName` property to the NPC's display name

## API Usage

```papyrus
; Simple chat
String response = CortexAPI.Chat("Hello traveler!", "Dragonborn")
String reply = CortexAPI.GetReply(response)
Debug.Notification("NPC: " + reply)

; With context
CortexAPI.InjectContext("Whiterun", "night", "rain")
response = CortexAPI.Chat("Is it safe outside?", "Dragonborn")

; Reset memory
CortexAPI.ForgetAll()
```

## NPC Emotions → Animations

| Emotion | Suggested Animation |
|---------|---------------------|
| `confident` | `IdleApplaud`, `IdleNod` |
| `neutral` | Default idle |
| `uncertain` | `IdleScratchHead`, `IdleThink` |
| `confused` | `IdleShrug`, `IdleHeadShake` |

## Example: Lydia with Memory

With Cortex, Lydia can remember your adventures:

```
Player: "Do you remember Bleak Falls Barrow?"
Lydia: "Of course, my Thane. We fought through draugr and 
       discovered the Dragonstone there. That was the day 
       you proved yourself as Dragonborn."
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No response | Check if Cortex.exe is running |
| "connection refused" | Verify port 8000 is not blocked |
| Scripts won't compile | Ensure SKSE source files are installed |
