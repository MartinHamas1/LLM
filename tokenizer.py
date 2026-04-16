from tokenizers import Tokenizer, models, trainers, pre_tokenizers, normalizers
from tokenizers.normalizers import NFKC, Lowercase, Sequence
from tokenizers.pre_tokenizers import Whitespace

def train_tokenizer(input_file, vocab_size=32000):
    tokenizer = Tokenizer(models.BPE())

    tokenizer.normalizer = Sequence([
        NFKC(),
        Lowercase()
    ])

    tokenizer.pre_tokenizer = Whitespace()

    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=[
            "[PAD]",
            "[UNK]",
            "[CLS]",
            "[SEP]",
            "[MASK]"
        ]
    )

    def batch_iterator():
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                yield line.strip()

    tokenizer.train_from_iterator(batch_iterator(), trainer=trainer)

    tokenizer.save("tokenizer.json")
    print("Tokenizer trained and saved!")

from tokenizers import Tokenizer

