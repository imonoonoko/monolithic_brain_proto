import time
import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from monolithic_brain import NeuralSymbolicBrain

def run_benchmark():
    model_id = "Qwen/Qwen2.5-1.5B"
    brain_path = "my_agent.brain"
    input_text = "The future of AI is"
    
    print(f"--- BENCHMARK: Base LLM vs Monolithic Brain ({model_id}) ---")
    
    # 1. Base LLM Benchmark
    print("\n[1] Benchmarking Base LLM (Vanilla)...")
    start_time = time.time()
    base_model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    load_time = time.time() - start_time
    print(f"    Load Time: {load_time:.4f}s")
    
    inputs = tokenizer(input_text, return_tensors="pt")
    
    # Warmup
    _ = base_model(**inputs)
    
    # Inference Latency
    latencies = []
    for _ in range(10):
        t0 = time.time()
        with torch.no_grad():
            outputs = base_model(**inputs)
        latencies.append(time.time() - t0)
    
    avg_base_latency = np.mean(latencies)
    print(f"    Avg Inference Latency (Forward Pass): {avg_base_latency*1000:.2f} ms")
    print(f"    Output Logits Shape: {outputs.logits.shape}")
    
    del base_model
    
    # 2. Monolithic Brain Benchmark
    print("\n[2] Benchmarking Monolithic Brain (LLM + HDC + ActInf)...")
    start_time = time.time()
    brain = NeuralSymbolicBrain.load_brain(brain_path, base_model=model_id, torch_dtype=torch.float32)
    brain.eval()
    load_time = time.time() - start_time
    print(f"    Load Time: {load_time:.4f}s")
    
    # Warmup
    _ = brain(inputs.input_ids)
    
    # Inference Latency
    latencies = []
    for _ in range(10):
        t0 = time.time()
        with torch.no_grad():
            results = brain(inputs.input_ids)
        latencies.append(time.time() - t0)
    
    avg_brain_latency = np.mean(latencies)
    print(f"    Avg Inference Latency (Forward Pass): {avg_brain_latency*1000:.2f} ms")
    
    # Overhead Calculation
    overhead = (avg_brain_latency - avg_base_latency) / avg_base_latency * 100
    print(f"\n--- RESULTS ---")
    print(f"Base Latency:  {avg_base_latency*1000:.2f} ms")
    print(f"Brain Latency: {avg_brain_latency*1000:.2f} ms")
    print(f"Overhead:      {overhead:.2f}%")
    print(f"Entropy:       {results['entropy'].item():.4f}")
    if results['needs_reflection'].item():
        print("ActInf Status: TRIGGERED (The brain decided to think)")
    else:
        print("ActInf Status: PASSIVE (The brain decided to act)")

if __name__ == "__main__":
    run_benchmark()
