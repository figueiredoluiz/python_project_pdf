import unittest
from unittest.mock import patch, MagicMock
import os
from src.utils.pdf_generator import PDFGenerator
from src.utils.custom_pdf import CustomPDF
from src.utils import file_utils

class TestPDFGenerator(unittest.TestCase):
    @patch('src.utils.pdf_generator.CustomPDF')
    @patch('src.utils.file_utils.FileUtils')
    @patch('os.path.getsize')
    def test_create_pdf_from_directory(self, mock_getsize, mock_file_utils, mock_custom_pdf):
        mock_file_utils.get_project_info.return_value = {'name': 'Test Project', 'version': '1.0.0'}
        mock_file_utils.get_gitignore_patterns.return_value = None
        mock_file_utils.get_file_structure.return_value = ['file1.txt', 'file2.py']
        mock_file_utils.is_binary.return_value = False
        mock_getsize.return_value = 100  # Simulate non-empty files

        mock_pdf = MagicMock()
        mock_custom_pdf.return_value = mock_pdf

        # Mock open to avoid actual file operations
        with patch('builtins.open', MagicMock()):
            PDFGenerator.create_pdf_from_directory('test_dir', 'output.pdf')

        mock_custom_pdf.assert_called_once_with('Project Documentation')
        mock_pdf.create_cover.assert_called_once()
        mock_pdf.add_page.assert_called()
        mock_pdf.chapter_title.assert_called()
        mock_pdf.chapter_body.assert_called()
        mock_pdf.output.assert_called_once_with('output.pdf')

    @patch('src.utils.pdf_generator.CustomPDF')
    @patch('src.utils.file_utils.FileUtils')
    def test_create_pdf_from_directory_with_binary_file(self, mock_file_utils, mock_custom_pdf):
        mock_file_utils.get_project_info.return_value = None
        mock_file_utils.get_gitignore_patterns.return_value = None
        mock_file_utils.get_file_structure.return_value = ['binary_file.bin']
        mock_file_utils.is_binary.return_value = True

        mock_pdf = MagicMock()
        mock_custom_pdf.return_value = mock_pdf

        PDFGenerator.create_pdf_from_directory('test_dir', 'output.pdf')

        mock_pdf.chapter_body.assert_called_with('Binary file')

    def test_replace_unsupported_characters(self):
        text = "This is a test… with ellipsis"
        result = PDFGenerator.replace_unsupported_characters(text)
        self.assertEqual(result, "This is a test... with ellipsis")

if __name__ == '__main__':
    unittest.main()