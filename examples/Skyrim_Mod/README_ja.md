# Skyrim用 Cortex NPC 統合ガイド

[🇺🇸 English](README.md)

Project Cortex を Skyrim Special Edition に統合するための Papyrus スクリプトです。

## 必要環境

- **Cortex.exe** が同じマシンで起動中（ポート8000）
- **SKSE64** (Skyrim Script Extender)
- Papyrus用 HTTP プラグイン:
  - [PapyrusHTTP](https://www.nexusmods.com/skyrimspecialedition/mods/)
  - [JContainers](https://www.nexusmods.com/skyrimspecialedition/mods/16495)

## ファイル構成

| ファイル | 説明 |
|----------|------|
| `CortexAPI.psc` | HTTP通信用コアAPIラッパー |
| `CortexNPC.psc` | NPC統合スクリプトのサンプル |

## セットアップ

1. **Cortex を起動:**
   ```bash
   Cortex.exe
   ```

2. **スクリプトをインストール:**
   - `.psc` ファイルを `Data/Scripts/Source/` にコピー
   - Creation Kit または Papyrus Compiler でコンパイル

3. **NPCにアタッチ:**
   - Creation Kit で `CortexNPC` スクリプトをNPCにアタッチ
   - `NPCName` プロパティにNPCの表示名を設定

## API 使用方法

```papyrus
; シンプルな会話
String response = CortexAPI.Chat("やあ、旅人！", "Dragonborn")
String reply = CortexAPI.GetReply(response)
Debug.Notification("NPC: " + reply)

; コンテキスト付き
CortexAPI.InjectContext("ホワイトラン", "夜", "雨")
response = CortexAPI.Chat("外は安全？", "Dragonborn")

; 記憶をリセット
CortexAPI.ForgetAll()
```

## NPC の感情 → アニメーション

| 感情 | 推奨アニメーション |
|------|-------------------|
| `confident` | `IdleApplaud`, `IdleNod` |
| `neutral` | デフォルトアイドル |
| `uncertain` | `IdleScratchHead`, `IdleThink` |
| `confused` | `IdleShrug`, `IdleHeadShake` |

## 例: 記憶を持つリディア

Cortex を使えば、リディアはあなたとの冒険を覚えています:

```
プレイヤー: 「ブリーク・フォール墓地のこと覚えてる？」
リディア: 「もちろんです、我が君。ドラウグルと戦い、
          ドラゴンストーンを発見したあの場所ですね。
          あなたがドラゴンボーンであると証明した日でした。」
```

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| 応答がない | Cortex.exe が起動しているか確認 |
| "connection refused" | ポート8000がブロックされていないか確認 |
| コンパイルエラー | SKSEソースファイルがインストールされているか確認 |
