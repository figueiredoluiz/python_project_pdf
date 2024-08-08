from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from html import escape

class CodeHighlighter:
    @staticmethod
    def highlight_code(content: str, file_extension: str) -> str:
        """
        Highlight the given code content based on the file extension.
        Args:
            content (str): The code content to highlight.
            file_extension (str): The file extension to determine the language.
        Returns:
            str: HTML string of the highlighted code.
        """
        try:
            lexer = get_lexer_by_name(file_extension)
        except ValueError:
            lexer = guess_lexer(content)
        
        formatter = HtmlFormatter(style='colorful', noclasses=True)
        highlighted_code = highlight(escape(content), lexer, formatter)
        
        # Wrap the highlighted code in a div
        return f'<div class="highlighted-code">{highlighted_code}</div>'