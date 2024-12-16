from PIL import Image, ImageDraw
from pathlib import Path
import pygame as pg
def make_image(container, tile_size, components):
    BASE_DIR = Path(__file__).absolute().parent
    img = Image.new("RGB", (container.w * tile_size[0], container.h * tile_size[1]), color = 'white')
    for key in components:
        texture = Image.open(key).convert("RGBA")
        texture = texture.resize((tile_size[0], tile_size[1]))
        for x, y in components[key]:
            img.paste(texture, (x*tile_size[0], y*tile_size[1]), mask=texture)

    img.save(BASE_DIR / "resources" / "images" / "map.jpg")





