import colorsys
import numpy as np


def hls_to_rgb(h, s, l):
    return [int(255 * i) for i in colorsys.hls_to_rgb(h, s, l)]


def rgb_to_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def hex_to_rgb(color):
    color = color.lstrip("#")
    length = len(color)
    return tuple(
        int(color[i : i + length // 3], 16) for i in range(0, length, length // 3)
    )


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
