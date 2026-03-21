# -*- coding: utf-8 -*-
import logging
import os
from odoo import models
from odoo.addons.sign.models.sign_request import SignRequestItemValue

_logger = logging.getLogger(__name__)

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False
    _logger.warning("Could not import arabic_reshaper or python-bidi. Arabic text in Sign will not work.")

# --- Correctly load the bundled font ---
try:
    # Build the path to the font file inside our module's static directory
    # os.path.dirname(__file__) is /path/to/addons/sign_arabic_fix/models
    # os.path.dirname(os.path.dirname(__file__)) is /path/to/addons/sign_arabic_fix
    font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'src', 'fonts', 'Amiri-Regular.ttf')
    
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Amiri', font_path))
        _logger.info("Successfully registered bundled Amiri font with reportlab.")
    else:
        _logger.error(f"FATAL: Amiri font file not found at expected path: {font_path}")
        ARABIC_SUPPORT = False # Disable Arabic support if font not found
        
except Exception as e:
    _logger.error(f"FATAL: Could not register bundled Amiri font. Error: {e}")
    ARABIC_SUPPORT = False # Disable Arabic support if font registration fails


# --- MONKEY PATCHING THE CORRECT FUNCTION: _render_on_pdf_canvas ---
# Save the original function from Odoo's code.
# The correct method name for Odoo 17 is _render_on_pdf_canvas
original_render_on_pdf_canvas = SignRequestItemValue._render_on_pdf_canvas


def _render_on_pdf_canvas_arabic(self, canvas, pdf_location):
    """
    This is our patched function that will replace the original.
    It checks for Arabic text, reshapes it, sets the font, and then calls
    the original Odoo function with the corrected text.
    """
    value_to_render = self.value
    
    if ARABIC_SUPPORT and isinstance(self.value, str):
        is_arabic = any('\u0600' <= char <= '\u06FF' for char in self.value)
        if is_arabic:
            _logger.info(f"Processing Arabic value for PDF rendering: '{self.value}'")
            # Set the canvas to use our registered Amiri font
            # It's crucial to set the font on the canvas directly
            canvas.setFont('Amiri', self.font_size)
            
            # Reshape the text for correct display
            reshaped_text = arabic_reshaper.reshape(self.value)
            bidi_text = get_display(reshaped_text)
            value_to_render = bidi_text
            _logger.info(f"Font set to Amiri and text reshaped to: '{value_to_render}'")
    
    # Temporarily set the value on the object for the original function call
    original_value = self.value
    self.value = value_to_render
    
    # Call the original Odoo function to do the actual drawing
    result = original_render_on_pdf_canvas(self, canvas, pdf_location)
    
    # Restore the original value of self.value
    self.value = original_value
    
    return result

# Here, we replace Odoo's function with our new, patched version.
SignRequestItemValue._render_on_pdf_canvas = _render_on_pdf_canvas_arabic


# We still need this empty class definition for the Odoo framework.
class SignRequestItem(models.Model):
    _inherit = 'sign.request.item'
    pass
