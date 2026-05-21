"""
Generate the VoiceSetu application icon.
Creates a simple microphone icon as .ico file.
Run this before building if assets/icon.ico doesn't exist.
"""

import os
import sys


def generate_icon():
    """Generate the application icon."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed. Installing...")
        os.system(f"{sys.executable} -m pip install Pillow")
        from PIL import Image, ImageDraw, ImageFont

    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        padding = size // 8
        cx = size // 2
        cy = size // 2

        # Background circle
        draw.ellipse(
            [padding, padding, size - padding, size - padding],
            fill=(41, 128, 185, 255),
        )

        # Microphone body (rounded rectangle approximation)
        mic_w = size // 5
        mic_h = size // 3
        mic_x1 = cx - mic_w
        mic_y1 = cy - mic_h
        mic_x2 = cx + mic_w
        mic_y2 = cy + mic_h // 4

        draw.rounded_rectangle(
            [mic_x1, mic_y1, mic_x2, mic_y2],
            radius=mic_w,
            fill=(255, 255, 255, 255),
        )

        # Microphone arc (stand)
        arc_margin = size // 6
        arc_y = cy + mic_h // 8
        draw.arc(
            [cx - arc_margin, arc_y - arc_margin // 2, cx + arc_margin, arc_y + arc_margin],
            start=0,
            end=180,
            fill=(255, 255, 255, 255),
            width=max(1, size // 20),
        )

        # Stand line
        line_top = arc_y + arc_margin
        line_bottom = line_top + size // 8
        draw.line(
            [cx, line_top, cx, line_bottom],
            fill=(255, 255, 255, 255),
            width=max(1, size // 20),
        )

        # Base line
        base_w = size // 5
        draw.line(
            [cx - base_w, line_bottom, cx + base_w, line_bottom],
            fill=(255, 255, 255, 255),
            width=max(1, size // 20),
        )

        images.append(img)

    # Ensure assets directory exists
    os.makedirs("assets", exist_ok=True)

    # Save as ICO
    ico_path = os.path.join("assets", "icon.ico")
    images[-1].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[:-1],
    )
    print(f"Icon generated: {ico_path}")

    # Also save a PNG version
    png_path = os.path.join("assets", "icon.png")
    images[-1].save(png_path, format="PNG")
    print(f"PNG icon generated: {png_path}")


if __name__ == "__main__":
    generate_icon()
