# test_batch_processing.py
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os


class TestBatchProcessing(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_content = """animal_type,name,age,color,months_in_shelter,behavior,health,vaccinated,target_audience
dog,Max,3,brown,2,friendly,good,True,families
cat,Luna,2,gray,3,playful,excellent,True,singles
dog,Rocky,4,black,5,energetic,good,False,active"""

        # Create test input CSV
        self.input_csv = os.path.join(self.temp_dir, "test_input.csv")
        with open(self.input_csv, 'w') as f:
            f.write(self.csv_content)

    def tearDown(self):
        """Clean up after each test."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_load_animals_from_csv(self):
        """Test loading animals from CSV with different ranges."""
        from content.chunked_generation.chunked_description_call import load_animals_from_csv

        # Test loading all animals
        animals = load_animals_from_csv(self.input_csv)
        self.assertEqual(len(animals), 3)

        # Test with start range
        animals = load_animals_from_csv(self.input_csv, parse_start=2)
        self.assertEqual(len(animals), 2)
        self.assertEqual(animals[0]['name'], 'Luna')

        # Test with end range
        animals = load_animals_from_csv(self.input_csv, parse_end=2)
        self.assertEqual(len(animals), 2)
        self.assertEqual(animals[-1]['name'], 'Luna')

        # Test with both ranges
        animals = load_animals_from_csv(self.input_csv, parse_start=2, parse_end=2)
        self.assertEqual(len(animals), 1)
        self.assertEqual(animals[0]['name'], 'Luna')

    def test_load_animals_invalid_file(self):
        """Test handling of invalid CSV file."""
        from chunked_description_call import load_animals_from_csv

        with self.assertRaises(Exception):
            load_animals_from_csv("nonexistent.csv")

    @patch('chunked_description_call.generate_animal_descriptions_batch')
    @patch('chunked_description_call.save_batch_descriptions')
    @patch('chunked_description_call.initialize_gemini')
    def test_process_animals_in_batches(self, mock_init, mock_save, mock_generate):
        """Test complete batch processing workflow."""
        from content.chunked_generation.chunked_description_call import process_animals_in_batches

        # Setup mocks
        mock_generate.return_value = "Test description"
        mock_save.return_value = "test_output.txt"
        mock_init.return_value = MagicMock()

        # Test with different batch sizes
        test_cases = [
            (1, 3),  # batch_size=1, expected_batches=3
            (2, 2),  # batch_size=2, expected_batches=2
            (3, 1),  # batch_size=3, expected_batches=1
        ]

        for batch_size, expected_batches in test_cases:
            # Reset mock counters
            mock_generate.reset_mock()
            mock_save.reset_mock()

            # Process batches
            process_animals_in_batches(
                input_csv_file=self.input_csv,
                batch_size=batch_size
            )

            # Verify number of calls
            self.assertEqual(
                mock_generate.call_count,
                expected_batches,
                f"With batch_size={batch_size}, expected {expected_batches} calls"
            )
            self.assertEqual(
                mock_save.call_count,
                expected_batches,
                f"With batch_size={batch_size}, expected {expected_batches} saves"
            )

    @patch('chunked_description_call.generate_animal_descriptions_batch')
    @patch('chunked_description_call.save_batch_descriptions')
    @patch('chunked_description_call.initialize_gemini')
    def test_process_animals_with_ranges(self, mock_init, mock_save, mock_generate):
        """Test batch processing with different ranges."""
        from content.chunked_generation.chunked_description_call import process_animals_in_batches

        # Create a test-specific output file in our temp directory
        test_output_file = os.path.join(self.temp_dir, "test_descriptions.txt")

        # Setup mocks
        mock_generate.return_value = "Test description"
        mock_save.return_value = test_output_file
        mock_init.return_value = MagicMock()

        # Test different range combinations
        test_cases = [
            (1, 2, 2),  # start=1, end=2, expected_animals=2
            (2, None, 2),  # start=2, end=None, expected_animals=2
            (None, 2, 2),  # start=None, end=2, expected_animals=2
            (1, 3, 3)  # start=1, end=3, expected_animals=3
        ]

        for start, end, expected_animals in test_cases:
            # Reset mock counters
            mock_generate.reset_mock()
            mock_save.reset_mock()

            # Clear the output file before each test case
            if os.path.exists(test_output_file):
                with open(test_output_file, 'w') as f:
                    f.write('')

            process_animals_in_batches(
                input_csv_file=self.input_csv,
                batch_size=1,  # Use batch_size=1 for easier testing
                parse_start=start,
                parse_end=end
            )

            # Verify number of calls matches number of animals in range
            self.assertEqual(
                mock_generate.call_count,
                expected_animals,
                f"With range {start}-{end}, expected {expected_animals} calls"
            )

            # Verify the output file exists and contains the expected number of batches
            if os.path.exists(test_output_file):
                with open(test_output_file, 'r') as f:
                    content = f.read()
                    batch_count = content.count("Batch")
                    self.assertEqual(
                        batch_count,
                        expected_animals,
                        f"Expected {expected_animals} batches in output file for range {start}-{end}"
                    )


if __name__ == '__main__':
    unittest.main(verbosity=2)