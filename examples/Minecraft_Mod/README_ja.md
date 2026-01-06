# Minecraft用 Cortex NPC 統合ガイド

[🇺🇸 English](README.md)

Project Cortex を Minecraft Mod に統合するためのサンプルコードです。

## 必要環境

- **Cortex.exe** が同じマシンで起動中（ポート8000）
- Lua対応のMinecraft Mod:
  - [ComputerCraft](https://www.curseforge.com/minecraft/mc-mods/computercraft)（推奨）
  - [OpenComputers](https://www.curseforge.com/minecraft/mc-mods/opencomputers)

## ファイル構成

| ファイル | 説明 |
|----------|------|
| `cortex_npc.lua` | API ラッパーと使用例 |

## クイックスタート

1. Cortex を起動:
   ```bash
   Cortex.exe
   ```

2. ゲーム内でコンピュータを作成し、実行:
   ```lua
   shell.run("cortex_npc")
   ```

## API 使用方法

```lua
-- NPCと会話
local result = CortexAPI.chat("こんにちは！", "Steve")
print(result.reply)      -- NPCの応答
print(result.emotion)    -- confident/neutral/uncertain/confused

-- ゲームコンテキストを注入
CortexAPI.inject({
    location = "村",
    time = "夜",
    weather = "雨"
})

-- 記憶をリセット
CortexAPI.forget()
```

## NPC の感情

| 感情 | 意味 | 推奨アニメーション |
|------|------|-------------------|
| `confident` | 自信あり | うなずき、笑顔 |
| `neutral` | 通常の会話 | アイドル |
| `uncertain` | 考え中 | 顎をかく |
| `confused` | 理解できない | 首を振る |

## ヒント

- **会話前にコンテキストを注入** すると、NPCが状況を把握できます
- **異なるspeakerを使用** して複数プレイヤーを追跡
- **memories_recalled** でNPCが何を覚えているか確認
