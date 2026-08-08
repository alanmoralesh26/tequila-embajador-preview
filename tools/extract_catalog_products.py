from pathlib import Path
from collections import deque

from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "img"


def polygon_cutout(source: Path, destination: Path, points: list[tuple[float, float]]) -> None:
    image = ImageOps.exif_transpose(Image.open(source)).convert("RGBA")
    width, height = image.size
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon([(round(x * width), round(y * height)) for x, y in points], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(max(2, width // 1800)))
    image.putalpha(mask)
    bounds = mask.getbbox()
    if bounds:
        pad = max(16, width // 140)
        left, top, right, bottom = bounds
        image = image.crop((max(0, left - pad), max(0, top - pad), min(width, right + pad), min(height, bottom + pad)))
    image.thumbnail((1200, 1600), Image.Resampling.LANCZOS)
    image.save(destination, optimize=True)


def white_cutout(source: Path, destination: Path) -> None:
    image = ImageOps.exif_transpose(Image.open(source)).convert("RGBA")
    width, height = image.size
    rgb = image.convert("RGB")
    px = rgb.load()
    background = bytearray(width * height)
    queue = deque()
    for x in range(width):
        queue.extend(((x, 0), (x, height - 1)))
    for y in range(height):
        queue.extend(((0, y), (width - 1, y)))
    while queue:
        x, y = queue.popleft()
        index = y * width + x
        if background[index]:
            continue
        red, green, blue = px[x, y]
        if min(red, green, blue) < 222 or max(red, green, blue) - min(red, green, blue) > 34:
            continue
        background[index] = 1
        if x: queue.append((x - 1, y))
        if x + 1 < width: queue.append((x + 1, y))
        if y: queue.append((x, y - 1))
        if y + 1 < height: queue.append((x, y + 1))
    alpha = Image.new("L", image.size, 255)
    alpha.putdata([0 if value else 255 for value in background])
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.7))
    image.putalpha(alpha)
    bounds = image.getchannel("A").getbbox()
    if bounds:
        image = image.crop(bounds)
    image.thumbnail((1200, 1600), Image.Resampling.LANCZOS)
    image.save(destination, optimize=True)


white_cutout(Path("/Users/alanmorales/Downloads/IMG_6393 2.JPG"), OUT / "el-general.png")

polygon_cutout(
    Path("/Users/alanmorales/Downloads/IMG_6379.JPG"),
    OUT / "reserva-penca.png",
    [
        (.455, .018), (.548, .018), (.563, .035), (.563, .145), (.546, .158),
        (.546, .315), (.560, .338), (.605, .365), (.630, .405), (.637, .900),
        (.620, .930), (.575, .948), (.425, .948), (.380, .930), (.363, .900),
        (.370, .405), (.395, .365), (.440, .338), (.454, .315), (.454, .158),
        (.437, .145), (.437, .035),
    ],
)

polygon_cutout(
    Path("/Users/alanmorales/Downloads/IMG_6384.JPG"),
    OUT / "viejos-amigos.png",
    [
        (.435, .043), (.565, .043), (.580, .060), (.580, .260), (.560, .281),
        (.560, .340), (.582, .365), (.635, .400), (.655, .445), (.655, .910),
        (.640, .938), (.600, .954), (.400, .954), (.360, .938), (.345, .910),
        (.345, .445), (.365, .400), (.418, .365), (.440, .340), (.440, .281),
        (.420, .260), (.420, .060),
    ],
)
