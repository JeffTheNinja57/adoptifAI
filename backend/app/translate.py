import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model = AutoModelForSeq2SeqLM.from_pretrained("../data")
tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-nl')


def translation_function(input_text):
    # return ""
    #
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
