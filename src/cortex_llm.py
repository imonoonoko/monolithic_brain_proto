import numpy as np
from llama_cpp import Llama
from typing import Generator, Tuple, List, Dict, Any, Optional
import config
from hippocampus import Hippocampus

class MonolithicCortex:
    """
    create_completion ストリームを使用した高レベルなモノリシック脳実装。
    logprobs を使用して能動的推論（Active Inference / エントロピー）を近似します。
    Hippocampus モジュールにより、思考パターンをHDCベクトルとして記憶化します。
    """
    def __init__(
        self, 
        model_path: str = config.MODEL_FILENAME,
        system_prompt: str = config.DEFAULT_PERSONA,
        n_ctx: int = config.CTX_SIZE,
        n_gpu_layers: int = 0
    ):
        print(f"[MonolithicCortex] モデルをロード中: {model_path}...")
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            embedding=False, 
            logits_all=True,
            verbose=False
        )
        self.system_prompt = system_prompt
        # 海馬モジュールの初期化 (Zero-Cost Memory)
        self.hippocampus = Hippocampus()
        print(f"[MonolithicCortex] 初期化完了。ペルソナ: {system_prompt[:30]}...")

    def calculate_entropy_from_logprobs(self, top_logprobs: Dict[str, float]) -> float:
        """
        APIから提供された top_k logprobs からシャノンエントロピーを計算します。
        思考の「迷い」や「不確実性」を数値化するために使用されます。
        """
        if not top_logprobs:
            return 0.0
            
        # 値（対数確率）を抽出
        log_probs = np.array(list(top_logprobs.values()))
        
        # 確率に変換
        probs = np.exp(log_probs)
        
        # 正規化（top_k のみで計算するため、合計が1.0になるように再調整）
        # これにより、上位候補の中での相対的な迷いを算出します。
        probs = probs / (np.sum(probs) + 1e-10)
        
        # エントロピー計算: -sum(p * log(p))
        entropy = -np.sum(probs * np.log(probs + 1e-10))
        return float(entropy)

    def think_stream(
        self, 
        user_input: str, 
        game_context: Optional[Dict[str, Any]] = None,
        max_tokens: int = 128,
        temperature: float = 0.4, # 0.3->0.4 少し緩和して表現の幅を広げる
        repeat_penalty: float = 1.05, # ループ防止のため1.05に設定（1.0だとループする）
        stop_tokens: List[str] = [
            "<|im_end|>", 
            "<|endoftext|>", 
            "User:", 
            "Human:", 
            "HumanHuman:", 
            "Assistant:", 
            "\n\n"
        ] # ストップワード強化
    ) -> Generator[Tuple[str, np.ndarray, float], None, None]:
        """
        思考ストリームを生成するジェネレータ。
        各ステップで (トークン文字列, 埋め込みベクトル, エントロピー値) を返します。
        """
        context_str = self._format_context(game_context)
        
        # Qwen ChatML Format
        # <|im_start|>system...<|im_end|><|im_start|>user...<|im_end|><|im_start|>assistant
        sys_content = f"{self.system_prompt}\n{context_str}"
        
        full_prompt = (
            f"<|im_start|>system\n{sys_content}<|im_end|>\n"
            f"<|im_start|>user\n{user_input}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )
        
        # create_completion をストリーミングモードかつ logprobs 有効で呼び出す
        stream = self.llm.create_completion(
            full_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            repeat_penalty=repeat_penalty,
            stop=stop_tokens,
            stream=True,
            logprobs=40 # 能動的推論 & 海馬記憶形成に必要
        )
        
        for chunk in stream:
            try:
                choice = chunk["choices"][0]
                text = choice["text"]
                
                # エントロピーの抽出 & 思考ベクトルの形成
                entropy = 0.0
                embedding = np.zeros(4096) # Default
                
                if "logprobs" in choice and choice["logprobs"] and "top_logprobs" in choice["logprobs"]:
                    # top_logprobs は List[Dict] (チャンク内のトークンごと。通常は1つ)
                    step_logprobs = choice["logprobs"]["top_logprobs"][0]
                    
                    # 1. Active Inference (Metacognition)
                    entropy = self.calculate_entropy_from_logprobs(step_logprobs)
                    
                    # 2. Hippocampus Projection (Zero-Cost Memory)
                    # 思考パターン(logprobs)を直接ベクトルに焼き付ける
                    embedding = self.hippocampus.project_thought(step_logprobs)
                
                yield text, embedding, entropy
                
                if choice["finish_reason"] is not None:
                    break
                    
            except KeyError:
                continue

    def _format_context(self, context: Optional[Dict[str, Any]]) -> str:
        if not context:
            return ""
        s = ", ".join([f"{k}={v}" for k, v in context.items()])
        return f"[System: Status={{{s}}}]"
