import requests
import json
import sys

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

url = "http://127.0.0.1:8000/chat"
payload = {
    "text": "こんにちは、自己紹介をお願いします。",
    "speaker": "Tester"
}
headers = {"Content-Type": "application/json"}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    print("\n--- API Response ---")
    print(f"Reply: {data['reply']}")
    print(f"Resonance: {data.get('resonance', 0)}%")
    print("--------------------")
    print("✅ 文字化けせずに表示されています。")
    
except Exception as e:
    print(f"Error: {e}")
