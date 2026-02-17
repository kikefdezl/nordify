#!/usr/bin/env python3
import argparse

import numpy as np
from PIL import Image, PngImagePlugin

PngImagePlugin.MAX_TEXT_CHUNK = 100 * 1024 * 1024  # 100 MB  # type: ignore

# Original Nord palette (16 colors)
NORD_PALETTE = [
    # Polar Night
    (46, 52, 64),  # nord0
    (59, 66, 82),  # nord1
    (67, 76, 94),  # nord2
    (76, 86, 106),  # nord3
    # Snow Storm
    (216, 222, 233),  # nord4
    (229, 233, 240),  # nord5
    (236, 239, 244),  # nord6
    # Frost
    (143, 188, 187),  # nord7
    (136, 192, 208),  # nord8
    (129, 161, 193),  # nord9
    (94, 129, 172),  # nord10
    # Aurora
    (191, 97, 106),  # nord11
    (208, 135, 112),  # nord12
    (235, 203, 139),  # nord13
    (163, 190, 140),  # nord14
    (180, 142, 173),  # nord15
]


def expand_palette(
    base_palette: list[tuple[int, int, int]],
    expansion_factor: int = 2,
) -> list[tuple[int, int, int]]:
    """
    Expand the palette by interpolating between existing colors.

    Args:
        base_palette: list of RGB tuples
        expansion_factor: How many intermediate colors to create between each pair

    Returns:
        Expanded palette with interpolated colors
    """
    expanded = list(base_palette)

    for i in range(len(base_palette)):
        for j in range(i + 1, len(base_palette)):
            color1 = np.array(base_palette[i])
            color2 = np.array(base_palette[j])

            # only interpolate between relatively close colors
            distance = np.linalg.norm(color1 - color2)
            if distance < 150:
                for step in range(1, expansion_factor):
                    alpha = step / expansion_factor
                    interp_color = (1 - alpha) * color1 + alpha * color2
                    expanded.append(tuple(interp_color.astype(int)))

    return expanded


def rgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    """
    Convert RGB to LAB color space for perceptually accurate color distance.

    Args:
        rgb: RGB values as numpy array (0-255)

    Returns:
        LAB values as numpy array
    """
    rgb = rgb / 255.0

    mask = rgb > 0.04045
    rgb_linear = np.where(mask, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)

    matrix = np.array(
        [
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041],
        ]
    )

    xyz = rgb_linear @ matrix.T

    xyz = xyz / np.array([0.95047, 1.00000, 1.08883])

    mask = xyz > 0.008856
    f_xyz = np.where(mask, xyz ** (1 / 3), 7.787 * xyz + 16 / 116)

    L = 116 * f_xyz[..., 1] - 16
    a = 500 * (f_xyz[..., 0] - f_xyz[..., 1])
    b = 200 * (f_xyz[..., 1] - f_xyz[..., 2])

    return np.stack([L, a, b], axis=-1)


def find_closest_color(
    pixel: np.ndarray,
    palette: list[tuple[int, int, int]],
    use_lab: bool = True,
) -> tuple[int, int, int]:
    """
    Find the closest color in the palette to the given pixel.

    Args:
        pixel: RGB pixel values (0-255)
        palette: list of RGB tuples
        use_lab: Use LAB color space for perceptually accurate matching

    Returns:
        Closest RGB color from palette
    """
    if use_lab:
        pixel_lab = rgb_to_lab(pixel.reshape(1, 1, 3)).reshape(3)
        palette_array = np.array(palette)
        palette_lab = rgb_to_lab(palette_array.reshape(1, -1, 3)).reshape(-1, 3)

        distances = np.linalg.norm(palette_lab - pixel_lab, axis=1)
    else:
        palette_array = np.array(palette)
        distances = np.linalg.norm(palette_array - pixel, axis=1)

    closest_idx = np.argmin(distances)
    return palette[closest_idx]


def convert_to_nord(
    image_path: str,
    output_path: str,
    expand: bool = True,
    expansion_factor: int = 3,
    use_lab: bool = True,
) -> None:
    """
    Convert an image to Nord palette.

    Args:
        image_path: Path to input image
        output_path: Path to save output image
        expand: Whether to expand the palette with interpolated colors
        expansion_factor: Number of intermediate colors between palette colors
        use_lab: Use perceptually accurate LAB color space
    """
    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img)

    palette = expand_palette(NORD_PALETTE, expansion_factor) if expand else NORD_PALETTE
    print(f"Using palette with {len(palette)} colors")

    height, width = img_array.shape[:2]
    output_array = np.zeros_like(img_array)

    print("Converting image...")
    for y in range(height):
        if y % 50 == 0:
            print(f"Progress: {y}/{height} rows")
        for x in range(width):
            pixel = img_array[y, x]
            output_array[y, x] = find_closest_color(pixel, palette, use_lab)

    output_img = Image.fromarray(output_array.astype("uint8"))
    output_img.save(output_path)
    print(f"Saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert images to Nord color palette")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument(
        "--no-expand", action="store_true", help="Use only original 16 Nord colors"
    )
    parser.add_argument(
        "--expansion-factor",
        type=int,
        default=3,
        help="Number of interpolated colors (default: 3)",
    )
    parser.add_argument(
        "--rgb-distance",
        action="store_true",
        help="Use RGB distance instead of perceptual LAB",
    )

    args = parser.parse_args()

    convert_to_nord(
        args.input,
        args.output,
        expand=not args.no_expand,
        expansion_factor=args.expansion_factor,
        use_lab=not args.rgb_distance,
    )


if __name__ == "__main__":
    main()
