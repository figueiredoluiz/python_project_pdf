import os

class Config:
    """
    Configuration class to store all constants and settings.
    """
    FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')

    FONTS = {
        'NotoSans': {
            '': os.path.join(FONT_DIR, 'NotoSans-Regular.ttf'),
            'B': os.path.join(FONT_DIR, 'NotoSans-Bold.ttf'),
            'I': os.path.join(FONT_DIR, 'NotoSans-Italic.ttf'),
        },
        'NotoSansCJK': {
            '': os.path.join(FONT_DIR, 'NotoSansCJKjp-Regular.otf'),
            'B': os.path.join(FONT_DIR, 'NotoSansCJKjp-Bold.otf'),
            'I': os.path.join(FONT_DIR, 'NotoSansCJKjp-Regular.otf'),
        },
        'NotoSansJP': {
            '': os.path.join(FONT_DIR, 'NotoSansJP-Regular.ttf'),
            'B': os.path.join(FONT_DIR, 'NotoSansJP-Bold.ttf'),
            'I': os.path.join(FONT_DIR, 'NotoSansJP-Regular.ttf'),
        },
    }

    DEFAULT_FONT = 'NotoSans'
    FALLBACK_FONTS = ['NotoSans', 'NotoSansCJK', 'NotoSansJP']

    FONT_SIZE_TITLE = 24
    FONT_SIZE_SUBTITLE = 18
    FONT_SIZE_HEADING = 16
    FONT_SIZE_SUBHEADING = 14
    FONT_SIZE_NORMAL = 12
    FONT_SIZE_SMALL = 10

    LINE_HEIGHT = 5

    TEMP_OUTPUT_FILE = 'temp_output.pdf'

    # New styling options
    TITLE_FONT_SIZE = 16
    TITLE_FONT_STYLE = 'B'
    TITLE_BACKGROUND_COLOR = (240, 240, 240)  # Light grey

    # Debug flag
    DEBUG = False