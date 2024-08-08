from fpdf import FPDF, XPos, YPos
import textwrap
from typing import Dict, Any
from ..config import Config

class CustomPDF(FPDF):
    """
    Custom PDF class for generating project documentation.
    """
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        if self.page_no() != 1:  # Skip header on cover page
            self.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_BOLD, Config.FONT_SIZE_SUBHEADING)
            self.cell(0, 10, self.title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            self.ln(10)

    def footer(self):
        # Footer will be added in a second pass
        pass

    def chapter_title(self, title: str):
        self.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_BOLD, Config.FONT_SIZE_SUBHEADING)
        self.multi_cell(0, 10, title)
        self.ln(10)

    def chapter_body(self, body: str, is_code: bool = False):
        self.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_NORMAL, Config.FONT_SIZE_SMALL)
        if is_code:
            # Split the code into lines and write each line
            lines = body.split('\n')
            for line in lines:
                self.cell(0, 5, line, 0, 1)
        else:
            self.multi_cell(0, 5, body)
        self.ln()

    def add_index_entry(self, text: str, link: int):
        self.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_NORMAL, Config.FONT_SIZE_BODY)
        self.set_text_color(0, 0, 255)
        self.cell(10, 5, chr(149), 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(0, 5, text, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, link=link)
        self.set_text_color(0)

    def create_cover(self, project_info: Dict[str, Any]):
        self.add_page()
        self.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_BOLD, Config.FONT_SIZE_TITLE)
        self.ln(60)
        self.cell(0, 20, project_info['name'], 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_NORMAL, Config.FONT_SIZE_SUBTITLE)
        self.cell(0, 10, f"version {project_info['version']}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(50)
        self.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_NORMAL, Config.FONT_SIZE_BODY)
        
        table_data = [
            ('Author', project_info.get('author')),
            ('Description', project_info.get('description')),
            ('License', project_info.get('license')),
            ('Homepage', project_info.get('homepage')),
            ('Repository', project_info.get('repository')),
            ('Keywords', ', '.join(project_info.get('keywords', [])) if project_info.get('keywords') else None)
        ]
        
        for key, value in table_data:
            if value:
                self.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_BOLD, Config.FONT_SIZE_BODY)
                self.cell(30, 8, key, 0)
                self.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_NORMAL, Config.FONT_SIZE_BODY)
                wrapped_value = textwrap.fill(str(value), width=70)
                self.multi_cell(0, 8, wrapped_value)
                self.ln(2)