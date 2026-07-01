"""
icon generator — two modes:
  1. python make_icon.py                        → draws the built-in red play-button
  2. python make_icon.py downloaded_icon.png    → converts YOUR image to icon.ico + icon.png
"""

from PIL import Image, ImageDraw


def make_frame(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ── Red rounded-square background ─────────────────────────────────────────
    pad = max(1, size // 12)
    radius = size // 5
    draw.rounded_rectangle(
        [pad, pad, size - pad, size - pad],
        radius=radius,
        fill=(233, 69, 96, 255),  # #e94560
    )

    # ── White play-button triangle ────────────────────────────────────────────
    cx, cy = size / 2, size / 2
    h = size * 0.42  # height of triangle
    w = h * 0.87  # width  (equilateral-ish)
    ox = size * 0.06  # nudge right so it looks centred visually

    triangle = [
        (cx - w / 2 + ox, cy - h / 2),  # top-left
        (cx - w / 2 + ox, cy + h / 2),  # bottom-left
        (cx + w / 2 + ox, cy),  # right tip
    ]
    draw.polygon(triangle, fill=(255, 255, 255, 255))
    return img


def build_ico(path: str = "icon.ico"):
    sizes = [16, 24, 32, 48, 64, 128, 256]
    frames = [make_frame(s) for s in sizes]
    frames[0].save(
        path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:],
    )
    print(f"Saved {path}  ({len(frames)} sizes: {sizes})")


def build_png(path: str = "icon.png", size: int = 256):
    """Save a single large PNG — used by tkinter's iconphoto."""
    img = make_frame(size)
    img.save(path, format="PNG")
    print(f"Saved {path}  ({size}x{size})")


def convert_image(src: str):
    """Convert any PNG/JPG/WEBP the user downloaded into icon.ico + icon.png."""
    import sys

    sizes = [16, 24, 32, 48, 64, 128, 256]

    base = Image.open(src).convert("RGBA")

    # Build every size with high-quality resampling
    frames = [base.resize((s, s), Image.LANCZOS) for s in sizes]

    frames[0].save(
        "icon.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:],
    )
    print(f"Saved icon.ico  ({len(frames)} sizes)")

    # 256 px PNG for tkinter iconphoto
    frames[-1].save("icon.png", format="PNG")
    print("Saved icon.png  (256x256)")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # User passed their downloaded image:  python make_icon.py myimage.png
        convert_image(sys.argv[1])
    else:
        # No argument — generate the built-in red play-button
        build_ico()
        build_png()
