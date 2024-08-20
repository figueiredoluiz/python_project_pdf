import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from src.main import print_usage, print_version, main

class TestMain(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_usage(self, mock_stdout):
        print_usage()
        expected_output = "Usage: project-pdf [--version] [--debug] <directory_path> <output_file>\n"
        expected_output += "Example: project-pdf --debug /path/to/project output.pdf\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('src.version.__version__', '1.0.0')
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_version(self, mock_stdout):
        print_version()
        self.assertEqual(mock_stdout.getvalue(), "project-pdf version 1.0.0\n")

    @patch('sys.argv', ['project-pdf', '--version'])
    @patch('src.main.print_version')
    def test_main_version(self, mock_print_version):
        main()
        mock_print_version.assert_called_once()

    @patch('sys.argv', ['project-pdf', '--debug', '/path/to/project', 'output.pdf'])
    @patch('src.main.PDFGenerator.create_pdf_from_directory')
    def test_main_create_pdf(self, mock_create_pdf):
        main()
        mock_create_pdf.assert_called_once_with('/path/to/project', 'output.pdf')

    @patch('sys.argv', ['project-pdf'])
    @patch('src.main.print_usage')
    def test_main_invalid_args(self, mock_print_usage):
        main()
        mock_print_usage.assert_called_once()

    @patch('sys.argv', ['project-pdf', '/path/to/project'])
    @patch('src.main.print_usage')
    def test_main_missing_output_file(self, mock_print_usage):
        main()
        mock_print_usage.assert_called_once()

if __name__ == '__main__':
    unittest.main()