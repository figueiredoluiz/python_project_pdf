import unittest
from src.utils.code_highlighter import CodeHighlighter

class TestCodeHighlighter(unittest.TestCase):
    def test_highlight_code(self):
        code = "print('Hello, world!')"
        highlighted_code = CodeHighlighter.highlight_code(code, 'py')
        self.assertIn('<div class="highlighted-code">', highlighted_code)
        self.assertIn('Hello, world!', highlighted_code)

if __name__ == '__main__':
    unittest.main()
