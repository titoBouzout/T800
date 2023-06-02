from transformers import pipeline
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# model = dir_path + "/codebert-base-mlm"
model = dir_path + "/models/codebert-javascript"

fill_mask = pipeline("fill-mask", model=model, tokenizer=model, device="cuda")


def codehint(s):
    return fill_mask(s)
