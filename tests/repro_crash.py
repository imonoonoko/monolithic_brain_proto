from llama_cpp import Llama
import config

def reproduce():
    print("Initializing...")
    llm = Llama(
        model_path=config.MODEL_FILENAME,
        embedding=True,
        verbose=True
    )
    tokens = [1, 2, 3, 4, 5]
    print(f"Eval tokens: {tokens}")
    llm.eval(tokens)
    print("Eval done.")
    print("Embeddings shape:", len(llm.embeddings()))

if __name__ == "__main__":
    reproduce()
