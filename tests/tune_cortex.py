import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cortex_llm import MonolithicCortex
import time

def run_tuning():
    print("--- パラメータチューニング・スイート ---")
    
    # 1回だけ初期化（モデルロード時間を節約）
    # 注: コンストラクタでパラメータを固定している場合は、think_stream 呼び出し時にオーバーライドできるように修正が必要かもしれないが、
    # 現在の cortex_llm.py は think_stream でパラメータを受け取る設計になっているのでOK。
    cortex = MonolithicCortex(system_prompt="あなたは親切なAIアシスタントです。")

    # テストするプロンプト
    prompt = "日本の四季の美しさについて、短く語ってください。"
    
    # グリッドサーチ設定
    penalties = [1.0, 1.02, 1.05, 1.1, 1.2]
    temperatures = [0.7] # 今回はpenaltyに焦点を当てる
    
    print(f"\nPrompt: {prompt}\n")
    print(f"{'Penalty':<10} | {'Temp':<5} | {'Output'}")
    print("-" * 80)

    for pen in penalties:
        for temp in temperatures:
            # 視認性のため、ストリーミングではなく一括取得のように振る舞う（実際はgeneratorを回す）
            response = ""
            start = time.time()
            
            # create_completion のパラメータは think_stream 経由で渡せるように cortex_llm.py が実装されている前提
            # 現在の cortex_llm.py を確認すると: 
            # think_stream(..., temperature, repeat_penalty, ...) となっている。
            
            stream = cortex.think_stream(
                user_input=prompt, 
                temperature=temp, 
                repeat_penalty=pen,
                max_tokens=64 # 短くテスト
            )
            
            for token, _, _ in stream:
                response += token
                
            elapsed = time.time() - start
            
            # 改行を削除して1行で表示
            clean_resp = response.replace("\n", " ").strip()[:60] + "..."
            
            print(f"{pen:<10} | {temp:<5} | {clean_resp}")

if __name__ == "__main__":
    run_tuning()
