import unittest
import os
from src.utils.file_utils import FileUtils

class TestFileUtils(unittest.TestCase):
    def test_get_file_extension(self):
        self.assertEqual(FileUtils.get_file_extension('file.txt'), 'txt')
        self.assertEqual(FileUtils.get_file_extension('archive.tar.gz'), 'gz')
        self.assertEqual(FileUtils.get_file_extension('no_extension'), '')

    def test_is_binary(self):
        with open('text_file.txt', 'w') as f:
            f.write('This is a text file.')
        self.assertFalse(FileUtils.is_binary('text_file.txt'))
        os.remove('text_file.txt')
        
        with open('binary_file.bin', 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04')
        self.assertTrue(FileUtils.is_binary('binary_file.bin'))
        os.remove('binary_file.bin')

    def test_get_gitignore_patterns(self):
        patterns = FileUtils.get_gitignore_patterns('.')
        self.assertIsNotNone(patterns)

    def test_get_file_structure(self):
        structure = FileUtils.get_file_structure('.')
        self.assertIsInstance(structure, list)

    def test_get_project_info(self):
        info = FileUtils.get_project_info('.')
        self.assertIsNone(info)

if __name__ == '__main__':
    unittest.main()
