import numpy as np

from main import expand_palette, find_closest_color, rgb_to_lab


def test_expand_palette_basic():
    base = [(0, 0, 0), (10, 10, 10)]
    expanded = expand_palette(base, expansion_factor=2)
    assert len(expanded) == 3
    assert (5, 5, 5) in expanded


def test_expand_palette_no_interpolation_if_far():
    base = [(0, 0, 0), (200, 200, 200)]
    expanded = expand_palette(base, expansion_factor=2)
    assert len(expanded) == 2


def test_rgb_to_lab_black():
    rgb = np.array([0, 0, 0])
    lab = rgb_to_lab(rgb)
    assert np.allclose(lab, [0, 0, 0], atol=1.0)


def test_rgb_to_lab_white():
    rgb = np.array([255, 255, 255])
    lab = rgb_to_lab(rgb)
    assert np.isclose(lab[0], 100, atol=1.0)


def test_find_closest_color_lab():
    palette = [(0, 0, 0), (255, 255, 255)]
    pixel = np.array([10, 10, 10])
    result = find_closest_color(pixel, palette, use_lab=True)
    assert result == (0, 0, 0)


def test_find_closest_color_rgb():
    palette = [(0, 0, 0), (255, 255, 255)]
    pixel = np.array([240, 240, 240])
    result = find_closest_color(pixel, palette, use_lab=False)
    assert result == (255, 255, 255)
