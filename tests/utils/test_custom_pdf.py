import unittest
from fpdf import FPDF
from src.utils.custom_pdf import CustomPDF

class TestCustomPDF(unittest.TestCase):
    def test_pdf_creation(self):
        pdf = CustomPDF('Test Title')
        pdf.add_page()
        pdf.chapter_title('Chapter 1')
        pdf.chapter_body('This is a test body.', is_code=False)
        self.assertEqual(pdf.page_no(), 1)

if __name__ == '__main__':
    unittest.main()
