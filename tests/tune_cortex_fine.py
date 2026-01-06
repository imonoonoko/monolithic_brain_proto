import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cortex_llm import MonolithicCortex
import time

def run_fine_tuning():
    print("--- 微調整チューニング (Repetition Penalty & Temp) ---")
    cortex = MonolithicCortex(system_prompt="あなたは賢明な哲学者です。") 
    
    # Prompt: 繰り返しが発生しやすい少し長めの回答を誘発する質問
    prompt = "人生の意味とは何ですか？"
    
    # Fine-grained grid
    penalties = [1.01, 1.02, 1.03, 1.04]
    temperatures = [0.3, 0.5]
    
    print(f"\nPrompt: {prompt}\n")
    print(f"{'Penalty':<10} | {'Temp':<5} | {'Output (First 80 chars)'}")
    print("-" * 100)

    for pen in penalties:
        for temp in temperatures:
            response = ""
            
            # cortex_llm.py の think_stream は引数でパラメータを上書きできる
            stream = cortex.think_stream(
                user_input=prompt, 
                temperature=temp, 
                repeat_penalty=pen,
                max_tokens=100
            )
            
            for token, _, _ in stream:
                response += token
                
            clean_resp = response.replace("\n", " ").strip()[:80] + "..."
            print(f"{pen:<10} | {temp:<5} | {clean_resp}")

if __name__ == "__main__":
    run_fine_tuning()
