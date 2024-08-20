import sys
import os
import logging
from src.config import Config
from src.utils.pdf_generator import PDFGenerator

def print_usage():
    print("Usage: project-pdf [--version] [--debug] <directory_path> <output_file>")
    print("Example: project-pdf --debug /path/to/project output.pdf")

def print_version():
    try:
        from src.version import __version__
    except ImportError:
        try:
            from version import __version__
        except ImportError:
            __version__ = "Unknown"
    print(f"project-pdf version {__version__}")

def main():
    """
    Main function to run the script.
    """
    if '--version' in sys.argv:
        print_version()
        return

    if '--debug' in sys.argv:
        Config.DEBUG = True
        sys.argv.remove('--debug')
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    if len(sys.argv) != 3:
        print_usage()
        return  # Exit after printing usage

    directory_path = sys.argv[1]
    output_file = sys.argv[2]

    try:
        PDFGenerator.create_pdf_from_directory(directory_path, output_file)
        print(f"PDF created successfully: {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if Config.DEBUG:
            print("Traceback:")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()