import os
import torch
import gc
import transformers
from threading import Timer


REPO = "Replit-v1-CodeInstruct-3B"
device = "cuda"


def get_tokenizer():
    global tokenizer
    if not tokenizer:
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            REPO, trust_remote_code=True, device_map="auto"
        )

    return tokenizer


def get_model():
    global model
    if not model:
        model = transformers.AutoModelForCausalLM.from_pretrained(
            REPO,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            init_device=device,
        )
        model.to(device)

    return model


def codegenerator(
    prompt,
    context,
):
    global tokenizer, model

    cancelTimeout()

    prompt = """### Instruction: {prompt}

### Input:
{context}

### Response:""".format(
        prompt=prompt,
        context=context,
    )
    tokenizer = get_tokenizer()
    model = get_model()

    eos_token_id = tokenizer.eos_token_id

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    generated_ids = model.generate(
        input_ids,
        max_new_tokens=768,
        # max_length=100,
        do_sample=True,
        use_cache=True,
        temperature=0.2,
        top_p=0.9,
        # top_k=4,
        eos_token_id=eos_token_id,
        pad_token_id=eos_token_id,
        #  num_return_sequences=1,
    )
    completion = tokenizer.decode(
        #  generated_ids[0]
        generated_ids[0][input_ids.shape[-1] :],
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )

    setTimeout(clear_cache, 10000)

    return completion.replace(context, "").replace(prompt, "")


t = False
tokenizer = False
model = False


def cancelTimeout():
    global t
    if t:
        t.cancel()


def setTimeout(fn, ms, *args, **kwargs):
    global t
    t = Timer(ms / 1000.0, fn, args=args, kwargs=kwargs)
    t.start()
    return t


def clear_cache():
    global tokenizer, model
    tokenizer = False
    model = False

    torch.cuda.empty_cache()

    gc.collect()


clear_cache()
