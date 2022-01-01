import imageio
from io import BytesIO
from typing import List, Tuple
from PIL.Image import Image as IMG
from PIL.ImageFont import FreeTypeFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .download import get_font, get_image

DEFAULT_FONT = 'SourceHanSansSC-Regular.otf'


def resize(img: IMG, size: Tuple[int, int]) -> IMG:
    return img.resize(size, Image.ANTIALIAS)


def rotate(img: IMG, angle: int, expand: bool = True) -> IMG:
    return img.rotate(angle, Image.BICUBIC, expand=expand)


def circle(img: IMG) -> IMG:
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((1, 1, img.size[0] - 2, img.size[1] - 2), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0))
    img.putalpha(mask)
    return img


def square(img: IMG) -> IMG:
    width, height = img.size
    length = min(width, height)
    return img.crop(((width - length) / 2, (height - length) / 2,
                     (width + length) / 2, (height + length) / 2))


def save_gif(frames: List[IMG], duration: float) -> BytesIO:
    output = BytesIO()
    imageio.mimsave(output, frames, format='gif', duration=duration)
    return output


def to_jpg(frame: IMG, bg_color=(255, 255, 255)) -> IMG:
    if frame.mode == 'RGBA':
        bg = Image.new('RGB', frame.size, bg_color)
        bg.paste(frame, mask=frame.split()[3])
        return bg
    else:
        return frame.convert('RGB')


def save_jpg(frame: IMG) -> BytesIO:
    output = BytesIO()
    frame = frame.convert('RGB')
    frame.save(output, format='jpeg')
    return output


def to_image(data: bytes, convert: bool = True) -> IMG:
    image = Image.open(BytesIO(data))
    if convert:
        image = square(to_jpg(image).convert('RGBA'))
    return image


async def load_image(name: str) -> IMG:
    image = await get_image(name)
    return Image.open(BytesIO(image)).convert('RGBA')


async def load_font(name: str, fontsize: int) -> FreeTypeFont:
    font = await get_font(name)
    return ImageFont.truetype(BytesIO(font), fontsize, encoding='utf-8')


async def text_to_pic(text: str, fontsize: int = 30, padding: int = 50,
                      bg_color=(255, 255, 255), font_color=(0, 0, 0)) -> BytesIO:
    font = await load_font(DEFAULT_FONT, fontsize)
    text_w, text_h = font.getsize_multiline(text)

    frame = Image.new('RGB', (text_w + padding * 2,
                      text_h + padding * 2), bg_color)
    draw = ImageDraw.Draw(frame)
    draw.multiline_text((padding, padding), text, font=font, fill=font_color)
    return save_jpg(frame)


async def fit_font_size(text: str, max_width: float, max_height: float,
                        fontname: str, max_fontsize: int, min_fontsize: int,
                        stroke_ratio: float = 0) -> int:
    fontsize = max_fontsize
    while True:
        font = await load_font(fontname, fontsize)
        width, height = font.getsize_multiline(
            text, stroke_width=int(fontsize * stroke_ratio))
        if width > max_width or height > max_height:
            fontsize -= 1
        else:
            return fontsize
        if fontsize < min_fontsize:
            return 0
