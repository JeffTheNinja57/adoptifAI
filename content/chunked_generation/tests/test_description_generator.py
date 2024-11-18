import unittest
from unittest.mock import patch, MagicMock
import os

from chunked_description_generator import generate_animal_descriptions_batch, initialize_gemini


class TestDescriptionGenerator(unittest.TestCase):
    def setUp(self):
        self.test_animal = {
            'row_num': 1,
            'animal_type': 'dog',
            'name': 'Max',
            'age': '3',
            'color': 'brown',
            'months_in_shelter': '2',
            'behavior': 'friendly',
            'health': 'good',
            'vaccinated': 'True',
            'target_audience': 'families'
        }

    @patch('google.generativeai.GenerativeModel')
    def test_initialize_gemini(self, mock_model):
        """Test Gemini model initialization."""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            model = initialize_gemini()
            self.assertIsNotNone(model)
            mock_model.assert_called_once()

    @patch('google.generativeai.GenerativeModel')
    def test_generate_descriptions_single_animal(self, mock_model):
        """Test generation for a single animal."""
        mock_response = MagicMock()
        mock_response.text = "Animal 1: Test description"
        mock_model.return_value.generate_content.return_value = mock_response

        result = generate_animal_descriptions_batch([self.test_animal])
        self.assertIn("Animal 1:", result)

    @patch('google.generativeai.GenerativeModel')
    def test_generate_descriptions_multiple_animals(self, mock_model):
        """Test generation for multiple animals."""
        animals = [
            self.test_animal,
            {**self.test_animal, 'row_num': 2, 'name': 'Luna'}
        ]
        mock_response = MagicMock()
        mock_response.text = "Animal 1: First description\nAnimal 2: Second description"
        mock_model.return_value.generate_content.return_value = mock_response

        result = generate_animal_descriptions_batch(animals)
        self.assertIn("Animal 1:", result)
        self.assertIn("Animal 2:", result)

    @patch('google.generativeai.GenerativeModel')
    def test_vaccinated_status_conversion(self, mock_model):
        """Test conversion of vaccinated status to Yes/No."""
        mock_response = MagicMock()
        mock_response.text = "Test"
        mock_model.return_value.generate_content.return_value = mock_response

        # Test with different vaccinated values
        test_cases = [
            ('True', 'Yes'),
            ('true', 'Yes'),
            ('False', 'No'),
            ('false', 'No')
        ]

        for input_val, expected in test_cases:
            animal = {**self.test_animal, 'vaccinated': input_val}
            generate_animal_descriptions_batch([animal])
            called_args = mock_model.return_value.generate_content.call_args[1]['contents']
            self.assertIn(f"vaccinated: {expected}", called_args)
