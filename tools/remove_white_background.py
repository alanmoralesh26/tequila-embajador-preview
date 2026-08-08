from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "assets" / "img"


def remove_white_background(source: Path, destination: Path) -> None:
    image = Image.open(source).convert("RGBA")
    pixels = []

    for red, green, blue, _ in image.getdata():
        distance_from_white = 255 - min(red, green, blue)
        alpha = max(0, min(255, round((distance_from_white - 5) * 255 / 22)))
        pixels.append((red, green, blue, alpha))

    image.putdata(pixels)
    alpha_channel = image.getchannel("A")
    bounds = alpha_channel.getbbox()
    if bounds:
        padding = 12
        left = max(0, bounds[0] - padding)
        top = max(0, bounds[1] - padding)
        right = min(image.width, bounds[2] + padding)
        bottom = min(image.height, bounds[3] + padding)
        image = image.crop((left, top, right, bottom))

    image.save(destination, optimize=True)


for product in ("platinum", "premium", "supreme"):
    remove_white_background(
        IMAGE_DIR / f"{product}-source.jpg",
        IMAGE_DIR / f"{product}.png",
    )
