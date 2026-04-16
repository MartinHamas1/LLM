from tokenizers import Tokenizer

tokenizer = Tokenizer.from_file("Medical_Tokenizer.json")

texts = [
    "Pacient trpí akútnou pankreatitídou a vyžaduje hospitalizáciu.",
    "Jsem student medicíny a učím se anatomii lidského těla.",
    "Příliš žluťoučký kůň úpěl ďábelské ódy.",
    "Dávka lieku bola 500 mg každých 8 hodín.",
]

for text in texts:
    tokens = tokenizer.encode(text)
    print("COUNT:", len(tokens))

