import os
from io import BytesIO
import PyPDF2
from fpdf import FPDF, XPos, YPos
from .file_utils import FileUtils
from .code_highlighter import CodeHighlighter
from .custom_pdf import CustomPDF
from ..config import Config

class PDFGenerator:
    """
    Main class for generating the PDF documentation.
    """
    @staticmethod
    def create_footer_page(page_num: int, total_pages: int) -> PyPDF2.PageObject:
        """
        Create a footer page with page numbers.

        Args:
            page_num (int): The current page number.
            total_pages (int): The total number of pages.

        Returns:
            PyPDF2.PageObject: A PDF page object with the footer.
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=False)
        pdf.add_page()
        pdf.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_ITALIC, Config.FONT_SIZE_SMALL)

        # Position the footer text at the bottom of the page
        footer_height = 10
        y_position = pdf.h - footer_height
        pdf.set_y(y_position)
        pdf.cell(0, footer_height, f'Page {page_num} of {total_pages}', 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='R')

        # Create an in-memory buffer
        buffer = BytesIO()
        pdf.output(buffer)
        buffer.seek(0)

        # Create a PdfReader object from the buffer
        return PyPDF2.PdfReader(buffer).pages[0]

    @classmethod
    def create_pdf_from_directory(cls, directory: str, output_file: str):
        """
        Create a PDF document from the contents of a directory.

        This function scans the given directory, creates a table of contents,
        and generates PDF pages for each file in the directory.

        Args:
            directory (str): Path to the directory to document.
            output_file (str): Path where the output PDF should be saved.
        """
        try:
            pdf = CustomPDF('Project Documentation')

            project_info = FileUtils.get_project_info(directory)
            if project_info:
                pdf.create_cover(project_info)

            gitignore_matcher = FileUtils.get_gitignore_patterns(directory)
            file_structure = FileUtils.get_file_structure(directory, gitignore_matcher)

            # Create table of contents
            pdf.add_page()
            pdf.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_BOLD, Config.FONT_SIZE_HEADING)
            pdf.cell(0, 10, 'Table of Contents', 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            pdf.ln(10)

            pdf.set_font(Config.FONT_FAMILY, Config.FONT_STYLE_BOLD, Config.FONT_SIZE_HEADING)
            pdf.cell(0, 10, 'File Structure', 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
            pdf.ln(5)

            links = {}
            for file_path in file_structure:
                link = pdf.add_link()
                links[file_path] = link
                pdf.add_index_entry(file_path, link)
                print(f"Created link for {file_path} -> {link}")  # Debugging output

            # Create file content pages
            for file_path in file_structure:
                pdf.add_page()
                link = links[file_path]
                pdf.set_link(link, y=pdf.get_y())  # Set link to the corresponding page and current y position
                pdf.chapter_title(file_path)
                print(f"Set link for {file_path} -> {link}")  # Debugging output

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
                            extension = FileUtils.get_file_extension(file_path)
                            highlighted_content = CodeHighlighter.highlight_code(content, extension)
                            pdf.chapter_body(highlighted_content, is_code=True)
                    except UnicodeDecodeError:
                        pdf.chapter_body('File contains non-UTF-8 encoded text')

            # Save the PDF without page numbers
            pdf.output(Config.TEMP_OUTPUT_FILE)

            # Second pass: Add page numbers
            with open(Config.TEMP_OUTPUT_FILE, 'rb') as temp_file, open(output_file, 'wb') as final_file:
                pdf_reader = PyPDF2.PdfReader(temp_file)
                pdf_writer = PyPDF2.PdfWriter()

                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    if page_num != 0:  # Skip footer on cover page
                        footer_page = cls.create_footer_page(page_num + 1, len(pdf_reader.pages))
                        page.merge_page(footer_page)
                    pdf_writer.add_page(page)

                pdf_writer.write(final_file)

        except Exception as e:
            print(f"An error occurred while creating the PDF: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(Config.TEMP_OUTPUT_FILE):
                os.remove(Config.TEMP_OUTPUT_FILE)
