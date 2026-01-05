from cortex_api import CortexBrainAPI

def awaken():
    """
    Refactored Awakening using the High-Level API.
    Used for quick verification.
    """
    print("\n--- Awakening Brain (API Mode) ---")
    
    # 1. Load via API
    brain = CortexBrainAPI()
    if not brain.load():
        print("Failed to awaken.")
        return

    # 2. Simulation Loop
    input_text = "自己紹介をお願いします。"
    print(f"\nPlayer: '{input_text}'")
    
    response = brain.think(input_text, game_context={"env": "testing"})
    
    # 3. Output
    print(f"\n[NPC Response]")
    print(f"Speech:      {response['speech']}")
    print(f"Action:      {response['action']}")
    print(f"Reflective:  {response['is_curious']}")
    
    # 4. Save
    brain.save()

if __name__ == "__main__":
    awaken()
