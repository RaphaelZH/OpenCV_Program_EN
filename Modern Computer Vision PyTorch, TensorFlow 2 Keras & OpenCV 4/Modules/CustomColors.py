import colorsys
import numpy as np


def hls_to_rgb(h, s, l):
    return [int(255 * i) for i in colorsys.hls_to_rgb(h, s, l)]


def rgb_to_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def hex_to_rgb(hex):
    hex = hex.lstrip("#")
    length = len(hex)
    return tuple(
        int(hex[i : i + length // 3], 16) for i in range(0, length, length // 3)
    )


def rgb_to_hls(rgb):
    r, g, b = tuple(i / 255 for i in rgb)
    return colorsys.rgb_to_hls(r, g, b)


def calm_color_generator(n):
    colors = []
    hue = np.repeat(np.random.random(), n)
    hue_interval = np.linspace(0, 1, n, endpoint=False)
    saturation = 0.6 + np.random.random() / 5.0 * np.random.choice([-1, 1])
    lightness = 0.5 + np.random.random() / 10.0 * np.random.choice([-1, 1])
    h = hue + hue_interval
    h = np.where(h > 1, h - 1, h)
    s = np.repeat(saturation, n)
    l = np.repeat(lightness, n)

    array_hls = np.concatenate((h, l, s)).reshape(-1, n).T
    for hls in array_hls:
        r, g, b = hls_to_rgb(hls[0], hls[1], hls[2])
        colors.append(rgb_to_hex(r, g, b))
    return colors


def gradient_dark_generator(color, n, color_space="hex"):
    colors = []
    if color_space == "hex":
        hsl = rgb_to_hls(hex_to_rgb(color))
    elif color_space == "rgb":
        hsl = rgb_to_hls(color)
    elif color_space == "hsl":
        color = (color[0], *[float(i.rstrip("%")) if type(i) == str else i for i in color[1:]])
        hsl = ([color[0] / 360, color[1] / 100, color[2] / 100])
    else:
        exception = Exception("This color space is not supported.")
        raise exception

    h, s = hsl[:2]
    h = np.repeat(h, n)
    s = np.repeat(s, n)
    l = np.linspace(0.9, 0.65, n, endpoint=False)

    array_hls = np.concatenate((h, l, s)).reshape(-1, n).T
    for hls in array_hls:
        r, g, b = hls_to_rgb(hls[0], hls[1], hls[2])
        colors.append(rgb_to_hex(r, g, b))
    return colors


"""
    

gradient light generator
"""
