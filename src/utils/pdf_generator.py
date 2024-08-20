import os
import traceback
from io import BytesIO
import PyPDF2
from fpdf import FPDF, XPos, YPos
from ..config import Config
from .custom_pdf import CustomPDF
import logging

logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    Main class for generating the PDF documentation.
    """
    @staticmethod
    def create_pdf_from_directory(directory: str, output_file: str):
        """
        Create a PDF document from the contents of a directory.
        """
        from .file_utils import FileUtils

        pdf = None
        try:
            if Config.DEBUG:
                logger.info(f"Starting PDF generation for directory: {directory}")
            pdf = CustomPDF('Project Documentation')

            project_info = FileUtils.get_project_info(directory)
            if project_info:
                if Config.DEBUG:
                    logger.info("Creating cover page")
                pdf.create_cover(project_info)

            gitignore_matcher = FileUtils.get_gitignore_patterns(directory)
            file_structure = FileUtils.get_file_structure(directory, gitignore_matcher)
            if Config.DEBUG:
                logger.info(f"Found {len(file_structure)} files to process")

            # Create table of contents
            if Config.DEBUG:
                logger.info("Creating table of contents")
            pdf.add_page()
            pdf.set_font(Config.DEFAULT_FONT, 'B', Config.FONT_SIZE_HEADING)
            pdf.cell(0, 10, 'Table of Contents', 0, 1, 'C')
            pdf.ln(5)

            pdf.set_font(Config.DEFAULT_FONT, '', Config.FONT_SIZE_SUBHEADING)
            pdf.cell(0, 10, 'File Structure', 0, 1, 'L')

            for file_path in file_structure:
                link = pdf.add_link()
                pdf.add_index_entry(file_path, link)

            # Create file content pages
            if Config.DEBUG:
                logger.info("Creating file content pages")
            for file_path in file_structure:
                if Config.DEBUG:
                    logger.debug(f"Processing file: {file_path}")
                pdf.add_page()
                pdf.chapter_title(file_path)

                full_path = os.path.join(directory, file_path)

                if os.path.basename(file_path) == 'package-lock.json':
                    pdf.chapter_body('package-lock.json content is ignored')
                elif FileUtils.is_binary(full_path):
                    pdf.chapter_body('Binary file')
                elif os.path.getsize(full_path) == 0:
                    pdf.chapter_body('File empty')
                else:
                    try:
                        with open(full_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            pdf.chapter_body(content)
                    except UnicodeDecodeError:
                        if Config.DEBUG:
                            logger.warning(f"File contains non-UTF-8 encoded text: {file_path}")
                        pdf.chapter_body('File contains non-UTF-8 encoded text')

            pdf.output(output_file)

            if Config.DEBUG:
                logger.info(f"PDF created successfully: {output_file}")
            print(f"PDF created successfully: {output_file}")

        except Exception as e:
            if Config.DEBUG:
                logger.error(f"An error occurred while creating the PDF: {str(e)}")
                logger.error("Traceback:", exc_info=True)
            print(f"An error occurred while creating the PDF: {str(e)}")
            print("Traceback:")
            traceback.print_exc()
            if os.path.exists(output_file):
                os.remove(output_file)
            print(f"Failed to create PDF: {output_file}")

    @staticmethod
    def replace_unsupported_characters(text: str):
        return text.replace("…", "...")