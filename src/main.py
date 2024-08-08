import sys
import os

def print_usage():
    print("Usage: project-pdf [--version] <directory_path> <output_file>")
    print("Example: project-pdf /path/to/project output.pdf")

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
    if len(sys.argv) == 2 and sys.argv[1] == '--version':
        print_version()
        sys.exit(0)

    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    directory_path = sys.argv[1]
    output_file = sys.argv[2]

    # Try different import methods
    try:
        # First, try importing normally (this works when running the script directly)
        from src.utils.pdf_generator import PDFGenerator
    except ImportError:
        try:
            # If that fails, try adding the current directory to the path
            # (this can work when running the compiled executable)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.insert(0, current_dir)
            from src.utils.pdf_generator import PDFGenerator
        except ImportError:
            # If that also fails, try importing without the 'src' prefix
            # (this can work if PyInstaller flattened the directory structure)
            try:
                from utils.pdf_generator import PDFGenerator
            except ImportError:
                print("Error: Unable to import required modules.")
                print("This might be due to running the compiled executable.")
                print("Please make sure you're running the script from the correct directory.")
                print_usage()
                sys.exit(1)

    try:
        PDFGenerator.create_pdf_from_directory(directory_path, output_file)
        print(f"PDF created successfully: {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()