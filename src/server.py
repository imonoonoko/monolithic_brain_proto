from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
import time
import os
import sys

# Ensure src is in path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex_llm import MonolithicCortex

app = FastAPI(title="CortexAI", version="1.0.0")

# --- Path Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # When in one-dir, this is inside internal
# If running as exe (onedir), we look relative to the exe location usually, 
# but PyInstaller unpacks to temp or runs in place. 
# For onedir, sys.executable is the exe path.
if getattr(sys, 'frozen', False):
    ROOT_DIR = os.path.dirname(sys.executable)
else:
    ROOT_DIR = os.getcwd() # Dev mode

MODELS_DIR = os.path.join(ROOT_DIR, "models")
MEMORIES_DIR = os.path.join(ROOT_DIR, "memories")

# Ensure directories exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(MEMORIES_DIR, exist_ok=True)

# Find Model
model_filename = "qwen-1.5b.gguf"
model_path = os.path.join(MODELS_DIR, model_filename)

if not os.path.exists(model_path):
    # Fallback to current dir for dev
    if os.path.exists(os.path.join(ROOT_DIR, "qwen2.5-1.5b-instruct-q4_k_m.gguf")):
         model_path = os.path.join(ROOT_DIR, "qwen2.5-1.5b-instruct-q4_k_m.gguf")
    else:
         print(f"WARNING: Model not found at {model_path}")
         # Attempt default
         model_path = "qwen2.5-1.5b-instruct-q4_k_m.gguf"

# --- Global Brain Instance ---
print("\n--- [CortexAI] Initializing Monolithic Brain... ---")
print(f"Loading Model: {model_path}")

# --- Persona Loading (Modder-friendly) ---
# Modderはこのファイルを編集することで、コードを触らずに性格を変更できます
PERSONA_FILE = os.path.join(ROOT_DIR, "persona.txt")
DEFAULT_PERSONA = "あなたは賢明な哲学者であり、プレイヤーの忠実な冒険仲間です。"

if os.path.exists(PERSONA_FILE):
    with open(PERSONA_FILE, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()
    print(f"[Persona] Loaded from persona.txt: {system_prompt[:50]}...")
else:
    system_prompt = DEFAULT_PERSONA
    print(f"[Persona] Using default: {DEFAULT_PERSONA[:50]}...")

brain = MonolithicCortex(
    system_prompt=system_prompt,
    model_path=model_path
)
current_context: Dict[str, Any] = {}

# --- Memory System ---
# STM: 短期記憶 (直近N発話を保持)
conversation_history: List[Dict[str, str]] = []
MAX_STM_SIZE = 5  # 保持する最大発話数

# LTM: 長期記憶 (永続ファイル)
LTM_FILE = os.path.join(MEMORIES_DIR, "ltm.json")

print("--- [Cortex-Linker] Brain is Awake. Ready to Link. ---\n")

# --- Data Models ---
class ChatRequest(BaseModel):
    text: str
    speaker: str = "Player"

class InjectRequest(BaseModel):
    info: Dict[str, Any]

# --- Console Visualizer ---
def log_brain_activity(speaker: str, message: str, emotion: str = None):
    """
    Simulates a high-tech console output for Modders.
    """
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {speaker:>10}: {message}")
    if emotion:
         print(f"             [Emotion]: {emotion}")

# --- Emotion System (Entropy-based) ---
def get_emotion_from_entropy(entropy: float) -> str:
    """
    エントロピー値から感情を推定する。
    低エントロピー = 確信 → confident
    高エントロピー = 迷い → confused
    """
    if entropy < 1.0:
        return "confident"   # 自信あり、はっきりした発言
    elif entropy < 2.0:
        return "neutral"     # 通常の会話
    elif entropy < 3.0:
        return "uncertain"   # やや迷い、考え中
    else:
        return "confused"    # 混乱、不確実

# --- API Endpoints ---

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    """
    [Main Function]
    Input: Player speech
    Output: NPC speech + Emotion
    Side-effect: Auto-memory recall & formation (STM + LTM)
    """
    global conversation_history
    
    log_brain_activity(req.speaker, req.text)
    
    # 0. Build STM context (直近の会話履歴をプロンプトに含める)
    stm_context = ""
    if conversation_history:
        stm_context = "\n[Recent Conversation]\n"
        for turn in conversation_history[-MAX_STM_SIZE:]:
            stm_context += f"- {turn['speaker']}: {turn['text']}\n"
    
    # 1. LTM Recall: 過去の類似記憶を検索
    ltm_context = ""
    recalled_memories = []
    # まず入力からクエリベクトルを作成（簡易版: 最初のトークンのlogprobsを使用）
    # 本格版ではEmbeddingモデルを使うが、ここではHippocampusの既存機能を活用
    
    # 2. Thinking Process (Stream -> Buffer)
    full_response = ""
    max_entropy = 0.0
    recalled = False
    thought_vectors = []  # 思考ベクトルを収集
    
    # STMを含んだ拡張コンテキスト
    extended_context = current_context.copy()
    if stm_context:
        extended_context["conversation_history"] = stm_context
    
    # Using the tuned parameters: Temp=0.4, Penalty=1.05
    stream = brain.think_stream(
        user_input=req.text, 
        game_context=extended_context,
        temperature=0.4,
        repeat_penalty=1.05
    )
    
    print("             [Cortex]: Thinking...", end="", flush=True)
    
    for token, vec, entropy in stream:
        full_response += token
        if entropy > max_entropy:
            max_entropy = entropy
        
        # 思考ベクトルを収集
        if vec.any():
            thought_vectors.append(vec)
            
        # LTM Recall: 生成中に類似記憶を検索
        if not recalled and vec.any():
            recalled_memories = brain.hippocampus.recall(vec, LTM_FILE, top_k=2)
            if recalled_memories:
                print(f"\n             [Hippocampus]: ⚡ Memory Recalled! ({len(recalled_memories)} matches) ⚡", end="")
                recalled = True
            
    print(" Done.")
    
    # 3. STM Update: 今回の発話を履歴に追加
    conversation_history.append({"speaker": req.speaker, "text": req.text})
    conversation_history.append({"speaker": "NPC", "text": full_response})
    
    # STMが上限を超えたら古いものを削除
    while len(conversation_history) > MAX_STM_SIZE * 2:
        conversation_history.pop(0)
    
    # 4. LTM Save: 重要な発話を長期記憶に保存
    # 重要度の判定: エントロピーを正規化（典型的なLLMのmax entropyは~4.0）
    normalized_entropy = min(max_entropy / 4.0, 1.0)  # 0.0-1.0に正規化
    importance = 1.0 - normalized_entropy
    if thought_vectors:  # 常に保存（テスト用）
        # 代表ベクトルとして全思考ベクトルの平均を使用
        import numpy as np
        avg_vector = np.mean(thought_vectors, axis=0)
        avg_vector = np.where(avg_vector >= 0, 1.0, -1.0)  # 二値化
        
        brain.hippocampus.save_memory(
            vector=avg_vector,
            user_input=req.text,
            response=full_response,
            filepath=LTM_FILE,
            importance=importance
        )
    
    # 5. Response
    log_brain_activity("NPC", full_response)
    
    # 想起した記憶があれば返す
    memories_recalled = [
        {"text": m[0].get("user_input", ""), "similarity": round(m[1], 2)}
        for m in recalled_memories
    ]
    
    return {
        "reply": full_response,
        "emotion": get_emotion_from_entropy(max_entropy),  # 動的感情検出
        "resonance": int((1.0 - max_entropy) * 100) if max_entropy < 1.0 else 0,
        "memories_recalled": memories_recalled
    }

@app.post("/inject")
def inject_endpoint(req: InjectRequest):
    """
    [Context Injection]
    Updates the brain's understanding of the world without direct speech.
    """
    global current_context
    current_context.update(req.info)
    print(f"             [System]: Context Injected -> {req.info}")
    return {"status": "ok", "current_context": current_context}

@app.post("/forget")
def forget_endpoint():
    """
    [Debug/Reset]
    Clears current context (and in future, short-term memory).
    """
    global current_context
    current_context = {}
    # TODO: brain.hippocampus.reset() if implemented
    print(f"             [System]: 🧹 Memory Wiped (Tabula Rasa)")
    return {"status": "wiped"}

if __name__ == "__main__":
    # 0.0.0.0 allows access from WSL/LAN if needed, but localhost is safer for mods
    uvicorn.run(app, host="127.0.0.1", port=8000)
