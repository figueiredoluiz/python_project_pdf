from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from html import escape

class CodeHighlighter:
    """
    Class for handling code highlighting.
    """
    @staticmethod
    def highlight_code(content: str, file_extension: str) -> str:
        """
        Highlight the given code content based on the file extension.
        """
        try:
            lexer = get_lexer_by_name(file_extension)
        except ValueError:
            lexer = guess_lexer(content)
        
        formatter = HtmlFormatter(style='colorful', noclasses=True)
        highlighted_code = highlight(escape(content), lexer, formatter)
        
        # Convert HTML to plain text with ANSI escape codes
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(highlighted_code, 'html.parser')
        plain_text = soup.get_text()
        
        return plain_text