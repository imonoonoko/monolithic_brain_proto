import threading
import queue
import time
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Tuple, Optional, Callable

class MemoryCortex(threading.Thread):
    """
    非同期メモリエンコーダー（海馬サブプロセス）。
    軽量モデル（SentenceTransformer）を使用して、メインスレッドをブロックせずに
    テキストをベクトル化（記憶化）します。
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        super().__init__(daemon=True)
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self.model_name = model_name
        self.running = True
        self.embedder = None
        self.is_ready = False

    def run(self):
        """
        バックグラウンドスレッドのメインループ。
        モデルをロードし、キューからテキストを取り出してベクトル化します。
        """
        print(f"[MemoryCortex] 軽量モデルをロード中: {self.model_name}...")
        try:
            self.embedder = SentenceTransformer(self.model_name)
            self.is_ready = True
            print(f"[MemoryCortex] 準備完了。バックグラウンドで記憶待機中。")
        except Exception as e:
            print(f"[MemoryCortex] モデルロード失敗: {e}")
            self.running = False
            return

        while self.running:
            try:
                # タイムアウト付きで取得することで、終了フラグを確認できる
                text = self.input_queue.get(timeout=1.0)
                
                # ベクトル化（CPUでも高速）
                vector = self.embedder.encode(text)
                
                # 結果を出力キューへ（必要ならコールバック発火も可）
                self.output_queue.put((text, vector))
                
                # デバッグ表示（本番では削除可）
                # print(f"[MemoryCortex] 記憶を作成: '{text[:20]}...' (Vector: {vector.shape})")
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[MemoryCortex] エンコードエラー: {e}")

    def memorize(self, text: str):
        """
        外部から記憶リクエストを送るメソッド。非ブロッキング。
        """
        if not self.running:
            print("[MemoryCortex] 警告: 停止しているため記憶できません。")
            return
        self.input_queue.put(text)

    def retrieve_memories(self) -> Optional[Tuple[str, np.ndarray]]:
        """
        作成された記憶（ベクトル）があれば取り出す。
        """
        try:
            return self.output_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        """
        スレッドを安全に停止する。
        """
        self.running = False
