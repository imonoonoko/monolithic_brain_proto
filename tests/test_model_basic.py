from llama_cpp import Llama
import config

def test_basic():
    print("Testing basic generation...")
    llm = Llama(
        model_path=config.MODEL_FILENAME,
        n_ctx=2048,
        verbose=False
    )
    prompt = "System: You are a helpful assistant.\nUser: Hello.\nAssistant:"
    output = llm.create_completion(prompt, max_tokens=20)
    print("Output:", output["choices"][0]["text"])

if __name__ == "__main__":
    test_basic()
