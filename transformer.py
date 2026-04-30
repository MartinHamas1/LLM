import os
import numpy as np
import tiktoken

input_file_path = 'Core_Medical_Text.txt'
with open(input_file_path, 'r', encoding='utf-8') as f:
    data = f.read()

enc = tiktoken.get_encoding("gpt2")
ids = enc.encode_ordinary(data)

n = len(ids)
train_ids = ids[:int(n*0.9)]
val_ids = ids[int(n*0.9):]

train_ids = np.array(train_ids, dtype=np.uint16)
val_ids = np.array(val_ids, dtype=np.uint16)

train_ids.tofile('train.bin')
val_ids.tofile('val.bin')

print(f"Použitý GPT-2 encoding (vocab size: {enc.n_vocab})")
print(f"train.bin vytvorený (dtype=uint16)")