# Cortex NPC Integration for Minecraft

[🇯🇵 日本語版](README_ja.md)

This folder contains example code for integrating Project Cortex with Minecraft mods.

## Requirements

- **Cortex.exe** running on the same machine (port 8000)
- A Lua-capable Minecraft mod:
  - [ComputerCraft](https://www.curseforge.com/minecraft/mc-mods/computercraft) (Recommended)
  - [OpenComputers](https://www.curseforge.com/minecraft/mc-mods/opencomputers)

## Files

| File | Description |
|------|-------------|
| `cortex_npc.lua` | Main API wrapper and examples |

## Quick Start

1. Start Cortex:
   ```bash
   Cortex.exe
   ```

2. In-game, create a Computer and run:
   ```lua
   shell.run("cortex_npc")
   ```

## API Usage

```lua
-- Chat with NPC
local result = CortexAPI.chat("Hello!", "Steve")
print(result.reply)      -- NPC's response
print(result.emotion)    -- confident/neutral/uncertain/confused

-- Inject game context
CortexAPI.inject({
    location = "Village",
    time = "night",
    weather = "rain"
})

-- Reset memory
CortexAPI.forget()
```

## NPC Emotions

| Emotion | Meaning | Suggested Animation |
|---------|---------|---------------------|
| `confident` | NPC is sure of their answer | Nod, smile |
| `neutral` | Normal conversation | Idle |
| `uncertain` | NPC is thinking | Scratch chin |
| `confused` | NPC doesn't understand | Shake head |

## Tips

- **Inject context before conversations** to make NPCs context-aware
- **Use different speakers** to track multiple players
- **Check `memories_recalled`** to see what the NPC remembers
