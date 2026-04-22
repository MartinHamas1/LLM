from tokenizers import Tokenizer

tokenizer = Tokenizer.from_file("tokenizer.json")

texts = [
    "Pacient trpí akútnou pankreatitídou a vyžaduje hospitalizáciu.",
    "Jsem student medicíny a učím se anatomii lidského těla.",
    "Příliš žluťoučký kůň úpěl ďábelské ódy.",
    "Dávka lieku bola 500 mg každých 8 hodín.",
]

for text in texts:
    encoding = tokenizer.encode(text)

    pieces = encoding.tokens
    ids = encoding.ids

    print("=" * 80)
    print("TEXT:")
    print(text)
    print()

    print("TOKENIZÁCIA:")
    print(" | ".join(pieces))
    print()

    print("TOKEN ID:")
    print(" | ".join(str(i) for i in ids))
    print()

    print(f"POČET TOKENOV: {len(ids)}")
    print("\n")
