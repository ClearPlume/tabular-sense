import os

from sentencepiece import SentencePieceProcessor


class Tokenizer:
    """词表处理器"""
    tokenizer: SentencePieceProcessor

    def __init__(self, vocab_file: str):
        if os.path.exists(vocab_file):
            self.tokenizer = SentencePieceProcessor()
            self.tokenizer.Load(vocab_file)
        else:
            raise FileNotFoundError(f"Vocab file not found: {vocab_file}")

    @property
    def vocab_size(self) -> int:
        return self.tokenizer.vocab_size()

    def piece_to_id(self, text: str) -> int:
        """编码单个token为id"""
        return self.tokenizer.PieceToId(text)

    def encode(self, text: str) -> list[int]:
        """编码文本为token ids"""
        return self.tokenizer.Encode(text)

    def decode(self, token_ids: list[int]) -> str:
        """解码token ids为文本"""
        return self.tokenizer.Decode(token_ids)
