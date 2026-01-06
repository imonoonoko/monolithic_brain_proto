from llama_cpp import Llama
import config

def reproduce_2():
    print("Initializing...")
    llm = Llama(
        model_path=config.MODEL_FILENAME,
        embedding=True, # The culprit?
        verbose=True
    )
    prompt = "Hello"
    print(f"Generating for: {prompt}")
    
    # Try generating 1 token
    output = llm.create_completion(prompt, max_tokens=1)
    print(f"Output: {output}")
    
    # Try accessing embeddings
    emb = llm.embeddings()
    print(f"Embeddings len: {len(emb) if emb else 'None'}")

if __name__ == "__main__":
    reproduce_2()
