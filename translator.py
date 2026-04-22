import numpy as np
import tiktoken

enc = tiktoken.get_encoding("gpt2")

with open("Final_Med_Data.txt", "r", encoding="utf-8") as f:
    text = f.read()

tokens = enc.encode(text)

data = np.array(tokens, dtype=np.uint16)

split = int(0.9 * len(data))

train = data[:split]
val = data[split:]

train.tofile("train.bin")
val.tofile("val.bin")
