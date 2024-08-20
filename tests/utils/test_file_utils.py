import unittest
from unittest.mock import patch, mock_open
import os
from src.utils.file_utils import FileUtils

class TestFileUtils(unittest.TestCase):
    def test_get_file_extension(self):
        self.assertEqual(FileUtils.get_file_extension('file.txt'), 'txt')
        self.assertEqual(FileUtils.get_file_extension('file.tar.gz'), 'gz')
        self.assertEqual(FileUtils.get_file_extension('file_without_extension'), '')

    @patch('builtins.open', new_callable=mock_open, read_data=b'test data')
    def test_is_binary_text_file(self, mock_file):
        self.assertFalse(FileUtils.is_binary('text_file.txt'))

    @patch('builtins.open', new_callable=mock_open, read_data=b'\x00\x01\x02\x03')
    def test_is_binary_binary_file(self, mock_file):
        self.assertTrue(FileUtils.is_binary('binary_file.bin'))

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='*.pyc\n__pycache__\n')
    def test_get_gitignore_patterns(self, mock_file, mock_isfile):
        mock_isfile.return_value = True
        patterns = FileUtils.get_gitignore_patterns('test_dir')
        self.assertIsNotNone(patterns)
        self.assertTrue(patterns.match_file('test.pyc'))
        self.assertTrue(patterns.match_file('__pycache__/file.py'))

    @patch('os.walk')
    @patch('os.path.relpath')
    def test_get_file_structure(self, mock_relpath, mock_walk):
        mock_walk.return_value = [
            ('root', ['dir1'], ['file1.txt', 'file2.py']),
            ('root/dir1', [], ['file3.md'])
        ]
        mock_relpath.side_effect = lambda x, y: x.replace('root/', '')

        file_structure = FileUtils.get_file_structure('root')
        expected_structure = ['dir1/file3.md', 'file1.txt', 'file2.py']
        self.assertEqual(file_structure, expected_structure)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"name": "Test Project", "version": "1.0.0"}')
    def test_get_project_info(self, mock_file, mock_exists):
        mock_exists.return_value = True
        project_info = FileUtils.get_project_info('test_dir')
        expected_info = {
            "name": "Test Project",
            "version": "1.0.0",
            "author": None,
            "description": None,
            "license": None,
            "homepage": None,
            "repository": None,
            "keywords": None
        }
        self.assertEqual(project_info, expected_info)

if __name__ == '__main__':
    unittest.main()