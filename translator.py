import numpy as np
from tokenizers import Tokenizer
import os

TOKENIZER_PATH = "Medical_Tokenizer.json"
TEXT_DATA_PATH = "Final_Med_Data.txt"

if not os.path.exists(TOKENIZER_PATH) or not os.path.exists(TEXT_DATA_PATH):
    print("Chyba: Uisti sa, že máš tokenizer a text v rovnakom priečinku!")
else:
    tokenizer = Tokenizer.from_file(TOKENIZER_PATH)

    print("Načítavam 36MB medicínskych dát...")
    with open(TEXT_DATA_PATH, "r", encoding="utf-8") as f:
        data = f.read()

    print("Tokenizujem text (premieňam slová na čísla)...")
    ids = tokenizer.encode(data).ids
    
    print(f"Počet vytvorených tokenov: {len(ids):,}")

    train_ids = np.array(ids, dtype=np.uint16)
    train_ids.tofile("train.bin")

    print("--- HOTOVO ---")
    print("Súbor 'train.bin' bol vytvorený.")
    print("Tento súbor teraz obsahuje celú tvoju medicínu v reči, ktorej rozumie AI.")