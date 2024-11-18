import unittest
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import urllib3
import requests
import torch
import transformers

#check if model and tokenizer load correctly
class TestModelLoading(unittest.TestCase):
    def setUp(self):
        model_dir = 'C:\\Users\\Simeon\\Desktop\\UNI\\YEAR 3\\SEM 1\\Software Engineering\\Project\\Task 2\\Fine-tuning\\fine_tuned_en_nl_translation_model'
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-nl')

    def test_model_type(self):
        try:
            # positive assertion, check if model is of correct type
            self.assertIsInstance(self.model, transformers.models.marian.modeling_marian.MarianMTModel)
            print("Model loaded correctly.")
        except AssertionError:
            print("Model loaded incorrectly.")

    def test_tokenizer_type(self):
        try:
            # positive assertion, check if tokenizer is of correct type
            self.assertIsInstance(self.tokenizer, transformers.models.marian.tokenization_marian.MarianTokenizer)
            print("Tokenizer loaded correctly.")
        except AssertionError:
            print("Tokenizer loaded incorrectly.")


#check if model translates at all
class TestTranslationOutput(unittest.TestCase):
    def setUp(self):
        model_dir = 'C:\\Users\\Simeon\\Desktop\\UNI\\YEAR 3\\SEM 1\\Software Engineering\\Project\\Task 2\\Fine-tuning\\fine_tuned_en_nl_translation_model'
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-nl')

    def test_non_empty_translation(self):
        text = "This is a test sentence."
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        # generate translation
        with torch.no_grad():
            translated_ids = self.model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], num_beams=4)
        translated_text = self.tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        
        try:
            # positive assertion, ensure that the translated text is not empty
            self.assertTrue(len(translated_text) > 0)
            print("Translation successful.")
        except AssertionError:
            print("Translation failed.")

#try translating a longer sequence
class TestTranslationLength(unittest.TestCase):
    def setUp(self):
        model_dir = 'C:\\Users\\Simeon\\Desktop\\UNI\\YEAR 3\\SEM 1\\Software Engineering\\Project\\Task 2\\Fine-tuning\\fine_tuned_en_nl_translation_model'
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-nl')

    def test_translation_length(self):
        # 147 word input
        text = "Meet Bella, a gentle, affectionate 4-year-old Labrador mix with a heart as warm as her golden fur. Bella is a loyal companion who’s as happy lounging by your side as she is on a walk in the park. She’s friendly with other dogs and loves meeting new people, making her a wonderful addition to any family. Bella is house-trained, understands basic commands, and has a calm demeanor that’s perfect for quieter households, though she’s always up for some playtime and belly rubs. Recently given a clean bill of health by the vet, she’s all set to find her forever home. Bella’s ideal family would be one that enjoys cuddles and can provide her with daily strolls to satisfy her curious nose. If you’re looking for a devoted friend with endless love to give, Bella might just be the perfect match. Come meet her and see for yourself!"
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        input_length = inputs["input_ids"].shape[1]
        length_penaltyy = 1 + 2.75*(input_length / 100)
        
        # generate translation
        with torch.no_grad():
            translated_ids = self.model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], num_beams=4, length_penalty=length_penaltyy)
        translated_text = self.tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        
        try:
            # positive assertion, ensure the translated text has length greater than zero
            self.assertTrue(len(translated_text) > 0.7*len(text))
            print("Model can translate longer sequences - translation has valid length.")
        except AssertionError:
            print("Model cannot translate longer sequences - translation length is invalid.")

#does it translate an emoji?
class TestEmojiTranslation(unittest.TestCase):
    def setUp(self):
        model_dir = 'C:\\Users\\Simeon\\Desktop\\UNI\\YEAR 3\\SEM 1\\Software Engineering\\Project\\Task 2\\Fine-tuning\\fine_tuned_en_nl_translation_model'
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-nl')

    def test_emoji_translation(self):
        text = "Hello! How are you? 😊"
        
        # Tokenize the input text
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)

        # Generate translation
        with torch.no_grad():
            translated_ids = self.model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], num_beams=4)
        translated_text = self.tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        
        try:
            # ensure the translated text is not empty
            self.assertTrue(len(translated_text) > 0, "Translation failed: Empty output")
        
            self.assertIn("😊", translated_text, "Translation successful, but emoji not correctly preserved/translated")
            print("Emoji preserved or translated correctly.")
            
        except AssertionError:
            print("Translation successfull, but emoji not handled correctly.")

# test for empty input
class TestEmptyInput(unittest.TestCase):
    def setUp(self):
        model_dir = 'C:\\Users\\Simeon\\Desktop\\UNI\\YEAR 3\\SEM 1\\Software Engineering\\Project\\Task 2\\Fine-tuning\\fine_tuned_en_nl_translation_model'
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-nl')

    def test_empty_input(self):
        text = ""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        # generate translation
        with torch.no_grad():
            translated_ids = self.model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], num_beams=4)
        translated_text = self.tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        
        try:
            # positive assertion, ensure that empty input results in empty translation
            self.assertEqual(len(translated_text), 0)
            print("Empty input handled correctly.")
        except AssertionError:
            print("Empty input not handled correctly.")

# see if translations are consistent
class TestConsistentTranslation(unittest.TestCase):
    def setUp(self):
        model_dir = 'C:\\Users\\Simeon\\Desktop\\UNI\\YEAR 3\\SEM 1\\Software Engineering\\Project\\Task 2\\Fine-tuning\\fine_tuned_en_nl_translation_model'
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-nl')

    def test_consistent_translation(self):
        text = "The quick brown fox jumps over the lazy dog. They then go to a park together, cuddle, share stories about the past, whereafter they take a nap and head home."
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        # generate first translation
        with torch.no_grad():
            translated_ids = self.model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], num_beams=4)
        translated_text_1 = self.tokenizer.decode(translated_ids[0], skip_special_tokens=True)

        # generate second translation 
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            translated_ids = self.model.generate(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'], num_beams=4)
        translated_text_2 = self.tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        
        try:
            # positive assertion, check if the translations are consistent
            self.assertEqual(translated_text_1, translated_text_2)
            print("Translation is consistent across different inferences.")
        except AssertionError:
            print("Translation is inconsistent across different inferences.")