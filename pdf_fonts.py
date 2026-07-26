# pdf_fonts.py
# Shared Arabic-capable font registration for every page that builds a PDF
# with reportlab. Import get_pdf_fonts() instead of duplicating the
# registration block in each page.

import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
_REGULAR_PATH = os.path.join(_FONT_DIR, "Amiri-Regular.ttf")
_BOLD_PATH = os.path.join(_FONT_DIR, "Amiri-Bold.ttf")

_registered = False


def get_pdf_fonts(lang: str):
    """
    Returns (font_regular_name, font_bold_name, fonts_available: bool).
    Registers Amiri once (cached) if lang == 'ar' and the files exist.
    Falls back to Helvetica (Latin-only) otherwise.
    """
    global _registered
    fonts_available = os.path.exists(_REGULAR_PATH) and os.path.exists(_BOLD_PATH)

    if lang == "ar" and fonts_available:
        if not _registered:
            pdfmetrics.registerFont(TTFont("Amiri", _REGULAR_PATH))
            pdfmetrics.registerFont(TTFont("Amiri-Bold", _BOLD_PATH))
            _registered = True
        return "Amiri", "Amiri-Bold", True

    return "Helvetica", "Helvetica-Bold", fonts_available