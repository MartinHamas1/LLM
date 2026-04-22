from tokenizers import Tokenizer, models, trainers, pre_tokenizers, normalizers
from tokenizers.normalizers import NFKC, Sequence
from tokenizers.pre_tokenizers import Whitespace


def train_tokenizer(input_file, vocab_size=32000):

    tokenizer = Tokenizer(models.BPE())

    tokenizer.normalizer = Sequence([
        NFKC()
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
            buffer = []

            for line in f:
                line = line.strip()

                if not line:
                    if buffer:
                        yield " ".join(buffer)
                        buffer = []
                    continue

                buffer.append(line)

            if buffer:
                yield " ".join(buffer)

    tokenizer.train_from_iterator(batch_iterator(), trainer=trainer)

    tokenizer.save("tokenizer.json")

    print("Tokenizer trained and saved!")
    
if __name__ == "__main__":
    train_tokenizer("Final_Med_Data.txt")
