import tiktoken

class TikTokenizer:
    def __init__(self, model="gpt-4o-mini"):
        self.enc = tiktoken.encoding_for_model(model)

    def encode(self, text):
        return self.enc.encode(text)

    def decode(self, tokens):
        return self.enc.decode(tokens)
    
tok = TikTokenizer()

texts = [
    "Pacient trpí akútnou pankreatitídou a vyžaduje hospitalizáciu.",
    "Jsem student medicíny a učím se anatomii lidského těla.",
    "Příliš žluťoučký kůň úpěl ďábelské ódy.",
    "Dávka lieku bola 500 mg každých 8 hodín.",
]

for text in texts:
    tokens = tok.encode(text)
    print("COUNT:", len(tokens))