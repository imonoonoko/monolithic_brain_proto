from llama_cpp import Llama
import config

def inspect():
    llm = Llama(model_path=config.MODEL_FILENAME, logits_all=True, verbose=False)
    print("Llama attributes:", dir(llm))
    
    llm.eval([1, 2, 3])
    # Try to find logits/scores
    # check for _scores
    if hasattr(llm, "_scores"):
        print("_scores found, shape:", getattr(llm, "_scores").shape)
    if hasattr(llm, "scores"):
        print("scores found, shape:", getattr(llm, "scores").shape)

if __name__ == "__main__":
    inspect()
