import unittest
from unittest.mock import patch, MagicMock
from content.chunked_generation.chunked_description_generator import generate_animal_descriptions_batch


class TestDescriptionGeneration(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_animal = {
            'row_num': 1,
            'animal_type': 'Dog',
            'name': 'Max',
            'age': 3,
            'color': 'Brown',
            'months_in_shelter': 2,
            'behavior': 'Friendly',
            'health': 'Good',
            'vaccinated': 'Yes',
            'target_audience': 'Families'
        }
        self.test_batch = [self.test_animal]

    def test_gemini_model_initialization(self):
        """Test 1: Verify Gemini model initialization"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            generate_animal_descriptions_batch(self.test_batch)
            mock_model.assert_called_once_with(
                "gemini-1.5-flash",
                system_instruction=unittest.mock.ANY
            )

    def test_single_animal_description(self):
        """Test 2: Verify single animal description generation"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_response = MagicMock()
            mock_response.text = "Animal 1: Max is a loving 3-year-old brown dog..."
            mock_model.return_value.generate_content.return_value = mock_response

            descriptions = generate_animal_descriptions_batch(self.test_batch)

            self.assertIn(1, descriptions)
            self.assertTrue(
                descriptions[1].startswith("Max is a loving"),
                "Description should start with the provided template"
            )

    def test_batch_processing(self):
        """Test 3: Verify batch processing capability"""
        test_batch = [
            self.test_animal,
            {**self.test_animal, 'row_num': 2, 'name': 'Luna'},
            {**self.test_animal, 'row_num': 3, 'name': 'Rocky'}
        ]

        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_response = MagicMock()
            mock_response.text = """
            Animal 1: Max is a loving dog...
            Animal 2: Luna is a sweet dog...
            Animal 3: Rocky is an energetic dog...
            """
            mock_model.return_value.generate_content.return_value = mock_response

            descriptions = generate_animal_descriptions_batch(test_batch)

            self.assertEqual(len(descriptions), 3, "Should generate descriptions for all animals")
            self.assertIn(2, descriptions, "Should contain description for second animal")

    def test_empty_batch_handling(self):
        """Test 4: Verify empty batch handling"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            empty_batch = []
            with self.assertRaises(ValueError):
                generate_animal_descriptions_batch(empty_batch)

    def test_long_description_handling(self):
        """Test 5: Verify handling of long input full_data"""
        long_behavior = "Extremely " + "very " * 50 + "friendly"
        test_animal = {**self.test_animal, 'behavior': long_behavior}

        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_response = MagicMock()
            mock_response.text = "Animal 1: Generated description..."
            mock_model.return_value.generate_content.return_value = mock_response

            descriptions = generate_animal_descriptions_batch([test_animal])
            self.assertIn(1, descriptions)
            self.assertTrue(len(descriptions[1]) <= 250, "Description should not exceed token limit")


class TestDescriptionIntegration(unittest.TestCase):
    """Integration tests for the description generation system"""

    def setUp(self):
        self.test_animal = {
            'row_num': 1,
            'animal_type': 'Dog',
            'name': 'Max',
            'age': 3,
            'color': 'Brown',
            'months_in_shelter': 2,
            'behavior': 'Friendly',
            'health': 'Good',
            'vaccinated': 'Yes',
            'target_audience': 'Families'
        }

    @patch('google.generativeai.GenerativeModel')
    def test_generation_to_file_pipeline(self, mock_model):
        """Integration Test 1: Test the complete pipeline from generation to file saving"""
        import os
        from datetime import datetime

        mock_response = MagicMock()
        mock_response.text = "Animal 1: Complete test description."
        mock_model.return_value.generate_content.return_value = mock_response

        # Generate description
        descriptions = generate_animal_descriptions_batch([self.test_animal])

        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = "test_descriptions"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"batch_1_{timestamp}.txt"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Batch 1 - Generated at {timestamp}\n")
            f.write("=" * 80 + "\n\n")
            for row_num, description in descriptions.items():
                f.write(f"Animal {row_num}:\n")
                f.write("-" * 40 + "\n")
                f.write(description + "\n\n")

        # Verify file exists and contains correct content
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Complete test description", content)

        # Cleanup
        os.remove(file_path)
        os.rmdir(output_dir)

    @patch('google.generativeai.GenerativeModel')
    def test_batch_generation_and_translation(self, mock_model):
        """Integration Test 2: Test batch generation with subsequent translation"""
        from your_translation_module import translate_text  # You'll need to import your translation function

        mock_response = MagicMock()
        mock_response.text = "Animal 1: Test description for translation."
        mock_model.return_value.generate_content.return_value = mock_response

        # Generate description
        descriptions = generate_animal_descriptions_batch([self.test_animal])

        # Mock translation
        with patch('your_translation_module.translate_text') as mock_translate:
            mock_translate.return_value = "Vertaalde testbeschrijving."

            # Translate each description
            translated_descriptions = {}
            for row_num, desc in descriptions.items():
                translated_descriptions[row_num] = translate_text(desc)

            self.assertIn(1, translated_descriptions)
            self.assertEqual(
                translated_descriptions[1],
                "Vertaalde testbeschrijving."
            )

    @patch('google.generativeai.GenerativeModel')
    def test_error_handling_and_logging(self, mock_model):
        """Integration Test 3: Test error handling and logging throughout the pipeline"""
        import logging

        # Set up logging
        logging.basicConfig(level=logging.DEBUG)

        # Mock an API error
        mock_model.return_value.generate_content.side_effect = Exception("API Error")

        # Attempt generation with error
        with self.assertLogs(level='ERROR') as log:
            with self.assertRaises(Exception):
                generate_animal_descriptions_batch([self.test_animal])

            self.assertTrue(any("API Error" in message for message in log.output))


if __name__ == '__main__':
    unittest.main(verbosity=2)