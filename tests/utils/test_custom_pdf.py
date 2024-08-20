import unittest
from unittest.mock import patch, MagicMock
from src.utils.custom_pdf import CustomPDF
from src.config import Config

class TestCustomPDF(unittest.TestCase):
    def setUp(self):
        self.pdf = CustomPDF('Test Title')
        self.pdf.add_page()  # Add a page before each test

    def test_init(self):
        self.assertEqual(self.pdf.title, 'Test Title')
        self.assertEqual(self.pdf.fallback_fonts, Config.FALLBACK_FONTS)

    @patch('src.utils.custom_pdf.FPDF.add_font')
    def test_initialize_fonts(self, mock_add_font):
        self.pdf.initialize_fonts()
        self.assertTrue(mock_add_font.called)

    @patch('src.utils.custom_pdf.FPDF.set_y')
    @patch('src.utils.custom_pdf.FPDF.cell')
    def test_footer(self, mock_cell, mock_set_y):
        self.pdf.footer()
        mock_set_y.assert_called_with(-15)
        mock_cell.assert_called()

    @patch('src.utils.custom_pdf.FPDF.set_font')
    @patch('src.utils.custom_pdf.FPDF.set_fill_color')
    @patch('src.utils.custom_pdf.FPDF.cell')
    def test_chapter_title(self, mock_cell, mock_set_fill_color, mock_set_font):
        self.pdf.chapter_title('Test Chapter')
        mock_set_font.assert_called()
        mock_set_fill_color.assert_called()
        mock_cell.assert_called()

    @patch('src.utils.custom_pdf.FPDF.set_font')
    @patch('src.utils.custom_pdf.FPDF.multi_cell')
    def test_chapter_body(self, mock_multi_cell, mock_set_font):
        self.pdf.chapter_body('Test Body')
        mock_set_font.assert_called()
        mock_multi_cell.assert_called()

    @patch('src.utils.custom_pdf.FPDF.set_font')
    @patch('src.utils.custom_pdf.FPDF.set_text_color')
    @patch('src.utils.custom_pdf.FPDF.cell')
    def test_add_index_entry(self, mock_cell, mock_set_text_color, mock_set_font):
        self.pdf.add_index_entry('Test Entry', 1)
        mock_set_font.assert_called()
        mock_set_text_color.assert_called()
        mock_cell.assert_called()

    @patch('src.utils.custom_pdf.FPDF.set_font')
    @patch('src.utils.custom_pdf.FPDF.cell')
    @patch('src.utils.custom_pdf.FPDF.multi_cell')
    def test_create_cover(self, mock_multi_cell, mock_cell, mock_set_font):
        project_info = {
            'name': 'Test Project',
            'version': '1.0.0',
            'author': 'Test Author',
            'description': 'Test Description'
        }
        self.pdf.create_cover(project_info)
        mock_set_font.assert_called()
        mock_cell.assert_called()
        mock_multi_cell.assert_called()

if __name__ == '__main__':
    unittest.main()