from fpdf import FPDF, XPos, YPos
import os
from typing import Dict, Any
from ..config import Config
import logging

logger = logging.getLogger(__name__)

class CustomPDF(FPDF):
    """
    Custom PDF class for generating project documentation with support for multiple languages and fallback fonts.
    """
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.set_auto_page_break(auto=True, margin=15)
        
        self.fallback_fonts = Config.FALLBACK_FONTS
        self.initialize_fonts()

        # Set the default font
        self.set_font(Config.DEFAULT_FONT, '', Config.FONT_SIZE_NORMAL)

        # Store total page count
        self.alias_nb_pages()

    def initialize_fonts(self):
        """
        Initialize fonts with different styles.
        """
        for font_name, font_styles in Config.FONTS.items():
            for style, font_file in font_styles.items():
                try:
                    if Config.DEBUG:
                        logger.debug(f"Initializing font: {font_name} (style: {style})")
                    self.add_font(font_name, style, font_file)
                    if Config.DEBUG:
                        logger.debug(f"Successfully initialized font: {font_name} (style: {style})")
                except Exception as e:
                    if Config.DEBUG:
                        logger.error(f"Could not load font {font_name} (style: {style}): {str(e)}")

    def header(self):
        pass  # We'll handle the header in the content section

    def footer(self):
        self.set_y(-15)
        self.set_font(Config.DEFAULT_FONT, '', Config.FONT_SIZE_SMALL)
        self.cell(0, 10, f'Page {self.page_no()} of {{nb}}', 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')

    def chapter_title(self, title: str):
        self.set_font(Config.DEFAULT_FONT, Config.TITLE_FONT_STYLE, Config.TITLE_FONT_SIZE)
        self.set_fill_color(*Config.TITLE_BACKGROUND_COLOR)
        self.cell(0, 10, title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L', fill=True)
        self.ln(5)

    def chapter_body(self, body: str):
        self.set_font(Config.DEFAULT_FONT, '', Config.FONT_SIZE_NORMAL)
        self.multi_cell(0, 5, body)
        self.ln()

    def add_index_entry(self, text: str, link: int):
        self.set_font(Config.DEFAULT_FONT, '', Config.FONT_SIZE_NORMAL)
        self.set_text_color(0, 0, 255)
        self.cell(10, 5, chr(149), 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.cell(0, 5, text, link=link)
        self.set_text_color(0)
        self.ln()

    def create_cover(self, project_info: Dict[str, Any]):
        self.add_page()
        self.set_font(Config.DEFAULT_FONT, 'B', Config.FONT_SIZE_TITLE)
        self.cell(0, 20, project_info['name'], 0, 1, 'C')
        self.set_font(Config.DEFAULT_FONT, '', Config.FONT_SIZE_SUBTITLE)
        self.cell(0, 10, f"version {project_info['version']}", 0, 1, 'C')
        self.ln(20)

        self.set_font(Config.DEFAULT_FONT, '', Config.FONT_SIZE_NORMAL)
        for key, value in project_info.items():
            if value and key not in ['name', 'version']:
                self.set_font(Config.DEFAULT_FONT, 'B', Config.FONT_SIZE_NORMAL)
                self.cell(30, 10, f"{key}:", 0)
                self.set_font(Config.DEFAULT_FONT, '', Config.FONT_SIZE_NORMAL)
                self.multi_cell(0, 10, str(value))