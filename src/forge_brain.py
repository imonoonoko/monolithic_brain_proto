import os
import urllib.request
from monolithic_brain import NeuralSymbolicBrain
import config


def download_model():
    if not os.path.exists(config.MODEL_FILENAME):
        print(f"Downloading base GGUF model from {config.MODEL_URL}...")
        urllib.request.urlretrieve(config.MODEL_URL, config.MODEL_FILENAME)
        print("Download complete.")
    else:
        print("Base GGUF model found.")


def forge():
    # 1. Ensure Body (GGUF Model) exists
    download_model()

    print("\n--- Forging Cortex Module ---")
    print("Initialize your AI's Personality.")
    print("1. English Knight")
    print("2. Japanese Samurai (日本語)")
    print("3. Custom")

    choice = input("Select Persona (1-3): ").strip()

    if choice == "1":
        system_prompt = "You are a noble Knight of the Cortex. You speak in formal English. You protect the user."
    elif choice == "2":
        system_prompt = "あなたは高潔な侍です。古風な日本語（〜でござる）で話します。主君（ユーザー）を守ります。"
    else:
        system_prompt = input("Enter Custom System Prompt: ").strip()

    # 2. Initialize Brain
    # This will create the HDC matrices and PFC settings
    print(f"\nForging new brain with cortex: {config.MODEL_FILENAME}...")
    print(f"System Prompt: {system_prompt}")
    brain = NeuralSymbolicBrain(model_path=config.MODEL_FILENAME)

    # Inject Persona
    brain.system_prompt = system_prompt

    # 3. Save the 'Soul' (Learned Parameters + Matrices)
    # The GGUF file remains separate (the body), the .brain file is the soul.
    brain.save_brain(config.BRAIN_FILENAME)
    print(f"Brain forged successfully! Soul saved to {config.BRAIN_FILENAME}")
    print(f"Required files to run: {config.MODEL_FILENAME} + {config.BRAIN_FILENAME}")


if __name__ == "__main__":
    forge()
