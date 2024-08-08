# Project Documentation Generator

This Python script generates a comprehensive PDF documentation of a project's file structure and contents. It's particularly useful for creating snapshots of project states or for using as a source for AI tools.

## Features

- Creates a cover page with project information from package.json (if available)
- Generates a table of contents with links to each file
- Includes the content of all text files
- Handles binary files and empty files appropriately
- Respects .gitignore rules
- Adds page numbers to the PDF

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/figueiredoluiz/python_project_pdf.git
   cd python_project_pdf
   ```

2. Build the application:
   ```
   make build
   ```

## Usage

Run the script from the command line, providing the path to the directory you want to document and the desired output PDF file name:

```
project-pdf /path/to/your/project output.pdf
```

For example:
```
project-pdf ../my-project my-project-docs.pdf
```

## How It Works

1. The script walks through the specified directory, respecting .gitignore rules.
2. It creates a PDF with a cover page (if package.json is found) and a table of contents.
3. For each file, it creates a new page in the PDF with the file's content.
4. Binary files and empty files are noted but their content is not included.
5. Page numbers are added in a second pass.

## Customization

You can customize the script by modifying the font styles and sizes at the top of the script file. Feel free to adjust these to match your preferences or branding.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback, please open an issue in the GitHub repository.