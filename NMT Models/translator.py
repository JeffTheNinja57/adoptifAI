#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Define the directory where the model and tokenizer are stored (adjust this to your directory)
def translate(input_text):
    model_dir = 'adjust as needed'
    # Model and tokenizer initially take upwards of 2.5 seconds to load, after the first load - around 1.7 seconds.
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-nl')

    text = str(input_text)
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    input_length = inputs["input_ids"].shape[1]
    length_penalty = 1 + 2.75 * (input_length / 100)  # 2.75 was established by trial and error

    # Generate translation (output will be token ids)
    with torch.no_grad():
        translated_ids = model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'],
                                        num_beams=4, length_penalty=length_penalty)

    # Decode the generated ids to text
    translation = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

    return translation


import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Or just having them as global variables, the model_dir can be adjusted as need be.
model = AutoModelForSeq2SeqLM.from_pretrained("Adjust to model directory")
tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-nl')


def translate(input_text):
    text = str(input_text)
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    input_length = inputs["input_ids"].shape[1]
    length_penalty = 1 + 2.75 * (input_length / 100)  # 2.75 was established by trial and error

    # Generate translation (output will be token ids)
    with torch.no_grad():
        translated_ids = model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'],
                                        num_beams=4, length_penalty=length_penalty)

    # Decode the generated ids to text
    translation = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

    return translation



import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def load_utilities(model_dir):
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-nl")
    return model, tokenizer


def translate(input_text, model, tokenizer):
    text = str(input_text)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    input_length = inputs["input_ids"].shape[1]
    length_penalty = 1 + 2.75 * (input_length / 100)  # 2.75 was established by trial and error

    # Generate translation (output will be token ids)
    with torch.no_grad():
        translated_ids = model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'],
                                        num_beams=4, length_penalty=length_penalty)

    # Decode the generated ids to text
    translation = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

    return translation
