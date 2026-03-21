# -*- coding: utf-8 -*-
import logging
from odoo import models
from odoo.addons.sign.models.sign_request import SignRequestItemValue

_logger = logging.getLogger(__name__)

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    # Register the Amiri font that we installed via apt_packages.txt
    # The path to system fonts in Debian/Ubuntu is usually here.
    try:
        # This will only run once when Odoo starts.
        pdfmetrics.registerFont(TTFont('Amiri', '/usr/share/fonts/truetype/amiri/Amiri-Regular.ttf'))
        _logger.info("Successfully registered Amiri font with reportlab for Sign App.")
    except Exception as e:
        _logger.error(f"Could not register Amiri font. Path might be wrong. Error: {e}")

    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False
    _logger.warning("Could not import arabic_reshaper, python-bidi, or reportlab components.")


# --- MONKEY PATCHING STARTS HERE ---
# We save the original functions first.
original_get_cairo_font_name_and_size = SignRequestItemValue._get_cairo_font_name_and_size
original_get_resampled_value = SignRequestItemValue._get_resampled_value


def _get_cairo_font_name_and_size_arabic(self, font_name='Helvetica', font_size=12, box_height=20):
    """
    This is our new function to force the font to be Amiri if Arabic is detected.
    """
    if ARABIC_SUPPORT and isinstance(self.value, str):
        is_arabic = any('\u0600' <= char <= '\u06FF' for char in self.value)
        if is_arabic:
            _logger.info("Arabic detected, forcing font to Amiri.")
            # Return 'Amiri' instead of the default font.
            return 'Amiri', min(font_size, box_height) * 0.8
    
    # If not Arabic, call the original Odoo function.
    return original_get_cairo_font_name_and_size(self, font_name, font_size, box_height)


def _get_resampled_value_arabic(self):
    """
    This is our new function to reshape the text before it gets rendered.
    """
    # First, get the value from the original Odoo function.
    value = original_get_resampled_value(self)
    
    if ARABIC_SUPPORT and isinstance(value, str):
        is_arabic = any('\u0600' <= char <= '\u06FF' for char in value)
        if is_arabic:
            _logger.info(f"Reshaping Arabic value: {value}")
            reshaped_text = arabic_reshaper.reshape(value)
            bidi_text = get_display(reshaped_text)
            return bidi_text
    
    return value


# Now, we replace the original Odoo functions with our new patched versions.
SignRequestItemValue._get_cairo_font_name_and_size = _get_cairo_font_name_and_size_arabic
SignRequestItemValue._get_resampled_value = _get_resampled_value_arabic


# We still need this empty class definition so Odoo recognizes the file as valid.
class SignRequestItem(models.Model):
    _inherit = 'sign.request.item'
    pass
