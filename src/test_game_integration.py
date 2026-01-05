from cortex_api import CortexBrainAPI
import time

def game_loop_simulation():
    # 1. Initialize API
    print("--- Game Engine: Starting NPC Subsystem ---")
    npc_brain = CortexBrainAPI(
        brain_path="my_agent.brain",
        model_path="qwen2.5-1.5b-instruct-q4_k_m.gguf"
    )
    
    if not npc_brain.load():
        print("Failed to load NPC. Exiting.")
        return

    # 2. Simulate Interactions
    interactions = [
        {"input": "こんにちは！いい天気ですね。", "context": {"location": "Village", "weather": "Sunny"}},
        {"input": "この近くに洞窟はありますか？", "context": {"location": "Village"}},
        {"input": "ありがとう。剣を抜いて準備します。", "context": {"location": "Forest", "player_action": "Draw Sword"}}
    ]
    
    for i, turn in enumerate(interactions):
        print(f"\n[Turn {i+1}] Player: {turn['input']}")
        print(f"       Context: {turn['context']}")
        
        # API Call
        start_time = time.time()
        response = npc_brain.think(turn['input'], game_context=turn['context'])
        elapsed = time.time() - start_time
        
        # Display Result
        print(f" >> NPC Speech: {response['speech']}")
        print(f" >> NPC Action: {response['action']}")
        print(f" >> Curiosity:  {response['is_curious']}")
        print(f" >> Latency:    {elapsed:.2f}s")
        
    # 3. Save State (Learning)
    print("\n--- Saving NPC State ---")
    npc_brain.save()
    print("--- Simulation Complete ---")

if __name__ == "__main__":
    game_loop_simulation()
