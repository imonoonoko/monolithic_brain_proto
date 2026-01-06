import numpy as np
import json
import os
import uuid
import base64
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class Hippocampus:
    """
    海馬 (Hippocampus) モジュール。
    LLMの思考パターン（Logprobs）を数学的に投影し、追加コスト「ゼロ」で
    思考ベクトル（Semantic Hypervector）を生成します。
    """
    def __init__(self, vocab_size: int = 152064, hdc_dim: int = 4096, seed: int = 42):
        """
        Args:
            vocab_size: モデルの語彙サイズ (Qwen2.5-1.5B は ~152k)
            hdc_dim: HDCベクトルの次元数
            seed: ランダム射影行列の固定シード
        """
        # 再現性のためシード固定
        np.random.seed(seed)
        
        # 射影行列: スパースなLogprobsを密なHDCベクトルへ変換
        # メモリ節約のため、使用時にオンデマンド生成するか、または軽量なハッシュ関数で代用も検討可能だが、
        # ここでは単純化のため行列を持つ (ただしスパースアクセスのため行列全体は保持せずとも良いが、実装を簡単にするため保持)
        # Note: 152k * 4k * float16 は巨大(1.2GB)になるため、
        # メモリ効率の良い「ハッシュ射影」または「固定ランダムシードからの動的生成」が理想。
        # 今回はMVPとして、クラス初期化時に行列を持たず、encode時に動的に計算する「擬似射影」を採用する。
        # (巨大な行列を持つとメモリ圧迫の原因になるため)
        
        self.vocab_size = vocab_size
        self.hdc_dim = hdc_dim
        self.seed = seed

    def project_thought(self, top_logprobs: Dict[str, float]) -> np.ndarray:
        """
        Logprobs (Top-K thinking pattern) を思考ベクトルに射影する。
        行列を持たず、トークンIDをシードとした乱数生成で射影をシミュレートする（メモリ消費ほぼゼロ）。
        """
        thought_vector = np.zeros(self.hdc_dim, dtype=np.float32)
        
        # 確率分布の正規化
        # APIからは対数確率が来る -> 確率に戻す
        log_probs = np.array(list(top_logprobs.values()))
        token_strs = list(top_logprobs.keys())
        
        # 数値安定性のためのMax引き
        probs = np.exp(log_probs - np.max(log_probs))
        probs = probs / (np.sum(probs) + 1e-10) # 正規化
        
        for i, token_str in enumerate(token_strs):
            p = probs[i]
            if p < 0.01: continue # 影響の小さいトークンは無視して高速化
            
            # トークン文字列をハッシュ化してシードにする（一貫性確保）
            # 注意: 文字列そのものを使うことで、TokenizerのID変更に強くなる
            token_seed = hash(token_str) % (2**32)
            
            # このトークン固有のベクトルを動的生成 (正規分布)
            rng = np.random.RandomState(token_seed)
            # バイポーラ (-1, 1) のスパースベクトルを生成して加算
            # 全次元作ると重いので、非ゼロ要素のみを選択的に加算する「Sparse Coding」的アプローチも可だが
            # ここではシンプルにランダムベクトル生成（サイズ小なら高速）
            token_vector = rng.choice([-1.0, 1.0], size=self.hdc_dim)
            
            thought_vector += p * token_vector
            
        # 二値化 (Bipolarize) してHDCの特性（ノイズ耐性）を得る
        # 0以上なら1, 未満なら-1
        bipolar_vector = np.where(thought_vector >= 0, 1.0, -1.0)
        
        return bipolar_vector

    def cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """
        2つの思考ベクトルの類似度を計算 (-1.0 ~ 1.0)
        """
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return np.dot(v1, v2) / (norm1 * norm2)

    # =========================================
    # 長期記憶 (LTM) 永続化機能
    # =========================================
    
    def _encode_vector(self, vec: np.ndarray) -> str:
        """ベクトルをBase64文字列にエンコード（ストレージ効率化）"""
        return base64.b64encode(vec.astype(np.float32).tobytes()).decode('ascii')
    
    def _decode_vector(self, encoded: str) -> np.ndarray:
        """Base64文字列からベクトルをデコード"""
        return np.frombuffer(base64.b64decode(encoded), dtype=np.float32)
    
    def save_memory(
        self, 
        vector: np.ndarray, 
        user_input: str, 
        response: str, 
        filepath: str,
        importance: float = 0.5
    ) -> str:
        """
        思考ベクトルとメタデータをLTMに保存する。
        
        Args:
            vector: 4096dim HDCベクトル
            user_input: ユーザーの発話
            response: NPCの応答
            filepath: 保存先JSONファイルパス
            importance: 重要度 (0.0-1.0)
        
        Returns:
            記憶のUUID
        """
        memories = self.load_memories(filepath)
        
        memory_id = str(uuid.uuid4())
        memory = {
            "id": memory_id,
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "vector": self._encode_vector(vector),
            "importance": importance
        }
        
        memories.append(memory)
        
        # 保存 (最大100件に制限してメモリ節約)
        if len(memories) > 100:
            # 重要度の低い古い記憶から削除
            memories.sort(key=lambda m: (m.get("importance", 0), m.get("timestamp", "")))
            memories = memories[-100:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(memories, f, ensure_ascii=False, indent=2)
        
        print(f"             [LTM]: 💾 Memory Saved (ID: {memory_id[:8]}...)")
        return memory_id
    
    def load_memories(self, filepath: str) -> List[Dict]:
        """LTMファイルから全記憶を読み込む"""
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    def recall(
        self, 
        query_vector: np.ndarray, 
        filepath: str, 
        top_k: int = 3,
        similarity_threshold: float = 0.3
    ) -> List[Tuple[Dict, float]]:
        """
        類似記憶を検索して想起する。
        
        Args:
            query_vector: 検索クエリとなる思考ベクトル
            filepath: LTMファイルパス
            top_k: 返す記憶の最大数
            similarity_threshold: 類似度の閾値
        
        Returns:
            [(記憶Dict, 類似度), ...] のリスト（類似度降順）
        """
        memories = self.load_memories(filepath)
        if not memories:
            return []
        
        results = []
        for mem in memories:
            try:
                stored_vec = self._decode_vector(mem["vector"])
                sim = self.cosine_similarity(query_vector, stored_vec)
                if sim >= similarity_threshold:
                    results.append((mem, sim))
            except (KeyError, ValueError):
                continue  # 破損した記憶はスキップ
        
        # 類似度でソートして上位K件を返す
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

