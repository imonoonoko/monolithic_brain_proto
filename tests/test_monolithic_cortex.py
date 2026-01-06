import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cortex_llm import MonolithicCortex
import time
import numpy as np

def test_stream():
    print("--- モノリシック・コーテックス (脳) を初期化中 ---")
    cortex = MonolithicCortex(
        system_prompt="あなたは賢明な哲学者です。" # 短く答えてはコード内で強制付与される
    )
    
    user_input = "人生の意味とは何ですか？"
    game_context = {"location": "古代ギリシャ", "hp": 100}
    
    print(f"\nユーザー: {user_input}")
    print(f"コンテキスト: {game_context}\n")
    print("--- 思考ストリーム開始 (With Hippocampus & Tuning) ---")
    
    start_time = time.time()
    token_count = 0
    
    print("NPC: ", end="", flush=True)
    
    first_vector = None
    
    for token, vector, entropy in cortex.think_stream(user_input, game_context=game_context, max_tokens=256):
        # トークンを即座に表示
        print(token, end="", flush=True)
        
        token_count += 1
        
        # ベクトルとエントロピーの型チェック
        assert isinstance(vector, np.ndarray), "Vector must be numpy array"
        assert vector.shape == (4096,), f"Vector shape mismatch: {vector.shape} (Expected 4096)"
        assert isinstance(entropy, float), "Entropy must be float"
        
        # 最初の非ゼロベクトルを保存して確認
        if first_vector is None and np.any(vector):
            first_vector = vector
            # print(f" [HDC Generated! dim={len(vector)}]", end="")
        
        # デバッグ: 最初の数トークンでエントロピーを表示する場合はここで行う
        if token_count <= 3:
            pass 
            
    end_time = time.time()
    duration = end_time - start_time
    tps = token_count / duration
    
    print(f"\n\n--- ストリーム完了 ---")
    print(f"トークン数: {token_count}")
    print(f"時間:       {duration:.2f}秒")
    print(f"速度:       {tps:.2f} トークン/秒")
    
    if first_vector is not None:
        print("✅ 海馬 (Hippocampus): 思考ベクトル生成を確認")
    else:
        print("⚠️ 海馬 (Hippocampus): ベクトルが全てゼロです (異常)")

    # パフォーマンス判定
    # 計算が増えたので基準を少し下げるが、ゼロコストなので大きくは落ちないはず
    if tps > 1.0:
        print("✅ パフォーマンス: OK")
    else:
        print("⚠️ パフォーマンス: 遅い")

if __name__ == "__main__":
    test_stream()
