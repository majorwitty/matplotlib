"""
Text layouting utilities.
"""

from .ft2font import KERNING_DEFAULT, LOAD_NO_HINTING


def layout(string, font, *, x0=0, kern_mode=KERNING_DEFAULT):
    """
    Render *string* with *font*.  For each character in *string*, yield a
    (character-index, x-position) pair.  When such a pair is yielded, the
    font's glyph is set to the corresponding character.

    Parameters
    ----------
    string : str
        The string to be rendered.
    font : FT2Font
        The font.
    x0 : float
        The initial x-value
    kern_mode : int
        A FreeType kerning mode.

    Yields
    ------
    character_index : int
    x_position : float
    """
    x = x0
    last_char_idx = None
    for char in string:
        char_idx = font.get_char_index(ord(char))
        kern = (font.get_kerning(last_char_idx, char_idx, kern_mode)
                if last_char_idx is not None else 0) / 64
        x += kern
        glyph = font.load_glyph(char_idx, flags=LOAD_NO_HINTING)
        yield char_idx, x
        x += glyph.linearHoriAdvance / 65536
        last_char_idx = char_idx
