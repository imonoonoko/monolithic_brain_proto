import torch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cortex_llm import MonolithicCortex
from hippocampus import Hippocampus

def verify_memory():
    model_filename = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
    
    # 1. Init Brain
    brain = NeuralSymbolicBrain(model_path=model_filename, n_ctx=2048)
    print("\n--- Cortex Memory Verification ---")
    
    # 2. Create Memories
    # We will manually inject "thoughts" to test HDC binding
    # Concept: "Apple" vs "Car"
    
    print("encoding 'Apple'...")
    embed_apple = brain.llm_embed.create_embedding("Apple")['data'][0]['embedding']
    hdc_apple = brain.hippocampus(embed_apple)
    brain.episodic_memory.add_memory(hdc_apple)
    
    print("encoding 'Red'...")
    embed_red = brain.llm_embed.create_embedding("Red")['data'][0]['embedding']
    hdc_red = brain.hippocampus(embed_red)
    brain.episodic_memory.add_memory(hdc_red)
    
    # 3. Test Recall
    print("\n--- Recall Test ---")
    
    # Query: Apple (Should match high)
    sim_apple = brain.episodic_memory.recall_memory(hdc_apple)
    print(f"Recall 'Apple': {sim_apple:.4f} (Expected: High)")
    
    # Query: Red (Should match high)
    sim_red = brain.episodic_memory.recall_memory(hdc_red)
    print(f"Recall 'Red':   {sim_red:.4f} (Expected: High)")
    
    # Query: Blue (Should be lower, unrelated)
    embed_blue = brain.llm_embed.create_embedding("Blue")['data'][0]['embedding']
    hdc_blue = brain.hippocampus(embed_blue)
    sim_blue = brain.episodic_memory.recall_memory(hdc_blue)
    print(f"Recall 'Blue':  {sim_blue:.4f} (Expected: Low/Noise)")
    
    if sim_apple > 0.1 and sim_blue < sim_apple:
        print("\n✅ Memory Superposition Verified: Can distinguish stored concepts from noise.")
    else:
        print("\n❌ Memory Verification Failed: Signal to noise ratio too low.")

if __name__ == "__main__":
    verify_memory()
