import unittest
import os
from src.utils.pdf_generator import PDFGenerator

class TestPDFGenerator(unittest.TestCase):
    def test_create_footer_page(self):
        footer_page = PDFGenerator.create_footer_page(1, 10)
        self.assertIsNotNone(footer_page)

    def test_create_pdf_from_directory(self):
        test_dir = 'test_dir'
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir, 'test_file.txt'), 'w') as f:
            f.write('Test content')
        
        output_file = 'output.pdf'
        PDFGenerator.create_pdf_from_directory(test_dir, output_file)
        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file)
        os.remove(os.path.join(test_dir, 'test_file.txt'))
        os.rmdir(test_dir)

if __name__ == '__main__':
    unittest.main()
