import unittest
import os
import tempfile
import shutil

from description_text import save_batch_descriptions


class TestDescriptionText(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.test_dir, "all_descriptions.txt")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_save_batch_descriptions_creates_file(self):
        """Test that batch descriptions are saved and file is created."""
        test_description = "Animal 1: Test description"
        file_path = save_batch_descriptions(
            test_description,
            1,
            self.output_file
        )

        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as f:
            content = f.read()
            self.assertIn("Batch 1", content)
            self.assertIn(test_description, content)

    def test_save_batch_descriptions_appends_content(self):
        """Test that new batches are appended to existing file."""
        desc1 = "Animal 1: First description"
        desc2 = "Animal 2: Second description"

        save_batch_descriptions(desc1, 1, self.output_file)
        save_batch_descriptions(desc2, 2, self.output_file)

        with open(self.output_file, 'r') as f:
            content = f.read()
            self.assertIn("Batch 1", content)
            self.assertIn("Batch 2", content)
            self.assertIn(desc1, content)
            self.assertIn(desc2, content)

    def test_save_batch_descriptions_invalid_path(self):
        """Test handling of invalid file path."""
        with self.assertRaises(Exception):
            save_batch_descriptions(
                "test",
                1,
                "/nonexistent/path/file.txt"
            )
