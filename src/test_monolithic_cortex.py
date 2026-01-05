from cortex_llm import MonolithicCortex
import time
import numpy as np

def test_stream():
    print("--- Initializing Monolithic Cortex ---")
    cortex = MonolithicCortex(
        system_prompt="You are a wise philosopher. Answer briefly."
    )
    
    user_input = "What is the meaning of life?"
    game_context = {"location": "Ancient Greece", "hp": 100}
    
    print(f"\nUser: {user_input}")
    print(f"Context: {game_context}\n")
    print("--- Thinking Stream Start ---")
    
    start_time = time.time()
    token_count = 0
    
    print("NPC: ", end="", flush=True)
    
    for token, vector, entropy in cortex.think_stream(user_input, game_context=game_context):
        # Print token immediately
        print(token, end="", flush=True)
        
        token_count += 1
        
        # Verify vector and entropy
        assert isinstance(vector, np.ndarray), "Vector must be numpy array"
        assert vector.shape == (1536,), f"Vector shape mismatch: {vector.shape}"
        assert isinstance(entropy, float), "Entropy must be float"
        
        # Optional: Print debug info for first few tokens
        if token_count <= 3:
            pass # print(f" [H:{entropy:.2f}]", end="")
            
    end_time = time.time()
    duration = end_time - start_time
    tps = token_count / duration
    
    print(f"\n\n--- Stream Complete ---")
    print(f"Tokens: {token_count}")
    print(f"Time:   {duration:.2f}s")
    print(f"Speed:  {tps:.2f} t/s")
    
    # Assert acceptable performance (CPU)
    # > 5 t/s is decent for 1.5B on CPU
    if tps > 1.0:
        print("✅ Performance: OK")
    else:
        print("⚠️ Performance: Slow")

if __name__ == "__main__":
    test_stream()
