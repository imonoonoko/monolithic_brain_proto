from memory_cortex import MemoryCortex
import time

def test_async():
    print("--- Memory Cortex (海馬) テスト開始 ---")
    memory = MemoryCortex()
    
    print("1. メモリ起動 (バックグラウンドロード)")
    memory.start()
    
    # モデルロード待ち（簡易同期）
    while not memory.is_ready:
        time.sleep(0.1)
        
    print("2. 思考しながら記憶リクエスト送信")
    memories_to_store = [
        "私はリンゴが好きだ。",
        "ここは暗くて寒い。",
        "勇者は剣を持っている。"
    ]
    
    start_time = time.time()
    
    for text in memories_to_store:
        print(f"Main Thread: '{text}' を記憶キューに追加")
        memory.memorize(text)
        # メインスレッドは止まらないことを確認（sleepなし）
        
    print(f"Main Thread: 全リクエスト送信完了 ({time.time() - start_time:.4f}秒)")
    print("Main Thread: 別の作業中 (Wait 3s)...")
    time.sleep(3)
    
    print("3. 記憶の回収")
    count = 0
    while True:
        result = memory.retrieve_memories()
        if result:
            text, vector = result
            print(f"Recalled: '{text}' -> Vector Shape: {vector.shape}")
            count += 1
        else:
            break
            
    print(f"合計 {count} 個の記憶をベクトル化しました。")
    memory.stop()
    print("--- テスト終了 ---")

if __name__ == "__main__":
    test_async()
