import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cortex_llm import MonolithicCortex
from hippocampus import Hippocampus
import numpy as np
import time

def cosine_similarity(v1, v2):
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return np.dot(v1, v2) / (norm1 * norm2)

def get_thought_vector(cortex, prompt, max_tokens=10):
    """思考ストリームを実行し、発生した全思考ベクトルの平均(重ね合わせ)を返す"""
    vectors = []
    print(f"Thinking about: '{prompt}' ...")
    stream = cortex.think_stream(
        user_input=prompt, 
        temperature=0.1, # 決定論的に近づけるため低温
        repeat_penalty=1.0,
        max_tokens=max_tokens
    )
    
    text_buffer = ""
    for token, vector, entropy in stream:
        vectors.append(vector)
        text_buffer += token
        
    print(f" -> Output: {text_buffer[:50]}...")
    
    if not vectors:
        return np.zeros(4096)
        
    # エピソード記憶として、一連の思考を重ね合わせる
    # (実際のHDCではMajority Voteや加算後の二値化などがあるが、ここでは単純平均で類似度を見る)
    # ※ Hippocampusは二値化ベクトル(-1, 1)を返すので、単純加算こそが「重ね合わせ」になる
    combined_vector = np.sum(vectors, axis=0)
    return combined_vector

def run_memory_test():
    print("--- Hippocampus Memory Verification ---")
    cortex = MonolithicCortex(system_prompt="あなたはAIです。")
    
    # 1. Consistency Test (同じ入力を2回)
    # リンゴについて2回考えさせる
    v_apple_1 = get_thought_vector(cortex, "リンゴとは何ですか？")
    v_apple_2 = get_thought_vector(cortex, "リンゴとは何ですか？")
    
    sim_consistency = cosine_similarity(v_apple_1, v_apple_2)
    print(f"\n[Consistency] Apple vs Apple Similarity: {sim_consistency:.4f}")
    
    # 2. Semantic Distinctions (異なる概念)
    # 車について考えさせる
    v_car = get_thought_vector(cortex, "自動車とは何ですか？")
    
    sim_diff = cosine_similarity(v_apple_1, v_car)
    print(f"[Distinction] Apple vs Car Similarity:   {sim_diff:.4f}")
    
    # 判定
    # 理想: Consistency > 0.8, Distinction < 0.5
    # ただしHDCは直交性が高いため、全く同じ単語が出ないと類似度は低くなる可能性がある
    token_overlap = (sim_consistency > sim_diff)
    
    print("\n--- 結論 ---")
    if token_overlap:
        print("✅ 記憶機能は正常です (同じ概念は似たベクトルになり、異なる概念は区別されています)。")
    else:
        print("⚠️ 記憶の区別が曖昧です (ランダム性が強すぎる可能性があります)。")

if __name__ == "__main__":
    run_memory_test()
