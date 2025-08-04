
import matplotlib.colors as mcolors


def high_contrast_color(color):
    """
    Returns 'black' or 'white' depending on which gives better contrast
    with the input color.
    """
    r, g, b = mcolors.to_rgb(color)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return 'black' if luminance > 0.5 else 'white'