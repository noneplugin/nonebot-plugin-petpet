import math
import httpx
import imageio
import cv2 as cv
import numpy as np
from enum import Enum
from io import BytesIO
from fontTools.ttLib import TTFont
from typing import Protocol, List, Tuple, Union
from typing_extensions import Literal
from PIL.Image import Image as IMG
from PIL.ImageFont import FreeTypeFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from emoji.unicode_codes import UNICODE_EMOJI

from .download import get_font, get_image
from .models import Command

DEFAULT_FONT = "SourceHanSansSC-Regular.otf"
BOLD_FONT = "SourceHanSansSC-Bold.otf"
EMOJI_FONT = "NotoColorEmoji.ttf"


def resize(img: IMG, size: Tuple[int, int]) -> IMG:
    return img.resize(size, Image.ANTIALIAS)


def rotate(img: IMG, angle: int, expand: bool = True) -> IMG:
    return img.rotate(angle, Image.BICUBIC, expand=expand)


def circle(img: IMG) -> IMG:
    img = square(img)
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((1, 1, img.size[0] - 2, img.size[1] - 2), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0))
    img.putalpha(mask)
    return img


def square(img: IMG) -> IMG:
    length = min(img.width, img.height)
    return cut_size(img, (length, length))


async def draw_text(
    img: IMG,
    pos: Tuple[float, float],
    text: str,
    font: FreeTypeFont,
    fill=None,
    spacing: int = 4,
    align: Literal["left", "right", "center"] = "left",
    stroke_width: int = 0,
    stroke_fill=None,
):
    if not text:
        return

    draw = ImageDraw.Draw(img)
    if all([char not in UNICODE_EMOJI["en"] for char in text]):
        draw.multiline_text(
            pos,
            text,
            font=font,
            fill=fill,
            spacing=spacing,
            align=align,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
        return

    emoji_font_file = BytesIO(await get_font(EMOJI_FONT))
    emoji_font = ImageFont.truetype(emoji_font_file, 109, encoding="utf-8")
    emoji_ttf = TTFont(emoji_font_file)

    def has_emoji(emoji: str):
        for table in emoji_ttf["cmap"].tables:  # type: ignore
            if ord(emoji) in table.cmap.keys():
                return True
        return False

    lines = text.strip().split("\n")
    max_w = font.getsize_multiline(text)[0]
    current_x, current_y = pos
    current_text = ""

    def draw_current_text():
        nonlocal current_x, current_text
        if current_text:
            draw.text(
                (current_x, current_y),
                current_text,
                font=font,
                fill=fill,
                stroke_width=stroke_width,
                stroke_fill=stroke_fill,
            )
            current_x += font.getsize(current_text)[0]
            current_text = ""

    for line in lines:
        line_w = font.getsize(line)[0]
        dw = max_w - line_w
        current_x = pos[0]
        if align == "center":
            current_x += dw / 2
        elif align == "right":
            current_x += dw

        for char in line:
            if char in UNICODE_EMOJI["en"] and has_emoji(char):
                draw_current_text()
                emoji_img = Image.new("RGBA", (150, 150))
                emoji_draw = ImageDraw.Draw(emoji_img)
                emoji_draw.text((0, 0), char, font=emoji_font, embedded_color=True)
                emoji_img = emoji_img.crop(emoji_font.getbbox(char))
                emoji_x, emoji_y = font.getsize(char)
                emoji_img = fit_size(
                    emoji_img, (emoji_x, emoji_y), FitSizeMode.INSIDE, FitSizeDir.SOUTH
                )
                img.paste(emoji_img, (int(current_x), int(current_y)), emoji_img)
                current_x += emoji_x
            else:
                current_text += char
        draw_current_text()
        current_y += font.getsize("A", stroke_width=stroke_width)[1] + spacing


# 适应大小模式
class FitSizeMode(Enum):
    INSIDE = 0  # 图片必须在指定的大小范围内
    INCLUDE = 1  # 图片必须包括指定的大小范围


# 适应大小方向
class FitSizeDir(Enum):
    CENTER = 0  # 居中
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    NORTHWEST = 5
    NORTHEAST = 6
    SOUTHWEST = 7
    SOUTHEAST = 8


def limit_size(
    img: IMG, size: Tuple[int, int], mode: FitSizeMode = FitSizeMode.INCLUDE
) -> IMG:
    """
    调整图片到指定的大小，不改变长宽比（即返回的图片大小不一定是指定的size）
    :params
      * ``img``: 待调整的图片
      * ``size``: 期望图片大小
      * ``mode``: FitSizeMode.INSIDE 表示图片必须在指定的大小范围内；FitSizeMode.INCLUDE 表示图片必须包括指定的大小范围
    """
    w, h = size
    img_w, img_h = img.size
    if mode == FitSizeMode.INSIDE:
        ratio = min(w / img_w, h / img_h)
    elif mode == FitSizeMode.INCLUDE:
        ratio = max(w / img_w, h / img_h)
    img_w = int(img_w * ratio)
    img_h = int(img_h * ratio)
    return resize(img, (img_w, img_h))


def cut_size(
    img: IMG,
    size: Tuple[int, int],
    direction: FitSizeDir = FitSizeDir.CENTER,
    bg_color: Union[str, float, Tuple[float, ...]] = (255, 255, 255, 0),
) -> IMG:
    """
    裁剪图片到指定的大小，超出部分裁剪，不足部分设为指定颜色
    :params
      * ``img``: 待调整的图片
      * ``size``: 期望图片大小
      * ``direction``: 调整图片大小时图片的方位；默认为居中 FitSizeDir.CENTER
      * ``bg_color``: FitSizeMode.INSIDE 时的背景颜色
    """
    w, h = size
    img_w, img_h = img.size
    x = int((w - img_w) / 2)
    y = int((h - img_h) / 2)
    if direction in [FitSizeDir.NORTH, FitSizeDir.NORTHWEST, FitSizeDir.NORTHEAST]:
        y = 0
    elif direction in [FitSizeDir.SOUTH, FitSizeDir.SOUTHWEST, FitSizeDir.SOUTHEAST]:
        y = h - img_h
    if direction in [FitSizeDir.WEST, FitSizeDir.NORTHWEST, FitSizeDir.SOUTHWEST]:
        x = 0
    elif direction in [FitSizeDir.EAST, FitSizeDir.NORTHEAST, FitSizeDir.SOUTHEAST]:
        x = w - img_w
    result = Image.new("RGBA", size, bg_color)
    result.paste(img, (x, y))
    return result


def fit_size(
    img: IMG,
    size: Tuple[int, int],
    mode: FitSizeMode = FitSizeMode.INCLUDE,
    direction: FitSizeDir = FitSizeDir.CENTER,
    bg_color: Union[str, float, Tuple[float, ...]] = (255, 255, 255, 0),
) -> IMG:
    """
    调整图片到指定的大小，超出部分裁剪，不足部分设为指定颜色
    :params
      * ``img``: 待调整的图片
      * ``size``: 期望图片大小
      * ``mode``: FitSizeMode.INSIDE 表示图片必须在指定的大小范围内，不足部分设为指定颜色；FitSizeMode.INCLUDE 表示图片必须包括指定的大小范围，超出部分裁剪
      * ``direction``: 调整图片大小时图片的方位；默认为居中 FitSizeDir.CENTER
      * ``bg_color``: FitSizeMode.INSIDE 时的背景颜色
    """
    return cut_size(limit_size(img, size, mode), size, direction, bg_color)


def perspective(img: IMG, points: List[Tuple[float, float]]):
    """
    透视变换
    :params
      * ``img``: 待变换的图片
      * ``points``: 变换后点的位置，顺序依次为：左上->右上->右下->左下
    """

    def find_coeffs(pa: List[Tuple[float, float]], pb: List[Tuple[float, float]]):
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
        A = np.matrix(matrix, dtype=np.float32)
        B = np.array(pb).reshape(8)
        res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
        return np.array(res).reshape(8)

    img_w, img_h = img.size
    points_w = [p[0] for p in points]
    points_h = [p[1] for p in points]
    new_w = int(max(points_w) - min(points_w))
    new_h = int(max(points_h) - min(points_h))
    p = [(0, 0), (img_w, 0), (img_w, img_h), (0, img_h)]
    coeffs = find_coeffs(points, p)
    return img.transform((new_w, new_h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)


def motion_blur(img: IMG, angle=0, degree=0) -> IMG:
    if degree == 0:
        return img.copy()
    matrix = cv.getRotationMatrix2D((degree / 2, degree / 2), angle + 45, 1)
    kernel = np.diag(np.ones(degree))
    kernel = cv.warpAffine(kernel, matrix, (degree, degree)) / degree
    blurred = cv.filter2D(np.asarray(img), -1, kernel)
    cv.normalize(blurred, blurred, 0, 255, cv.NORM_MINMAX)
    return Image.fromarray(np.array(blurred, dtype=np.uint8))


def distort(img: IMG, coefficients: Tuple[float, float, float, float]) -> IMG:
    res = cv.undistort(
        np.asarray(img),
        np.array([[100, 0, img.width / 2], [0, 100, img.height / 2], [0, 0, 1]]),
        np.asarray(coefficients),
    )
    return Image.fromarray(np.array(res, dtype=np.uint8))


def color_mask(img: IMG, color: Tuple[int, int, int]) -> IMG:
    img = img.convert("RGB")
    w, h = img.size
    img_array = np.asarray(img)
    img_gray = cv.cvtColor(img_array, cv.COLOR_RGB2GRAY)
    img_hsl = cv.cvtColor(img_array, cv.COLOR_RGB2HLS)
    img_new = np.zeros((h, w, 3), np.uint8)
    r, g, b = color
    rgb_sum = sum(color)
    for i in range(h):
        for j in range(w):
            value = img_gray[i, j]
            new_color = [
                int(value * r / rgb_sum),
                int(value * g / rgb_sum),
                int(value * b / rgb_sum),
            ]
            img_new[i, j] = new_color
    img_new_hsl = cv.cvtColor(img_new, cv.COLOR_RGB2HLS)
    result = np.dstack((img_new_hsl[:, :, 0], img_hsl[:, :, 1], img_new_hsl[:, :, 2]))
    result = cv.cvtColor(result, cv.COLOR_HLS2RGB)
    return Image.fromarray(result)


def save_gif(frames: List[IMG], duration: float) -> BytesIO:
    output = BytesIO()
    imageio.mimsave(output, frames, format="gif", duration=duration)
    return output


def to_jpg(frame: IMG, bg_color=(255, 255, 255)) -> IMG:
    if frame.mode == "RGBA":
        bg = Image.new("RGB", frame.size, bg_color)
        bg.paste(frame, mask=frame.split()[3])
        return bg
    else:
        return frame.convert("RGB")


def save_jpg(frame: IMG) -> BytesIO:
    output = BytesIO()
    frame = frame.convert("RGB")
    frame.save(output, format="jpeg")
    return output


class Maker(Protocol):
    async def __call__(self, img: IMG) -> IMG:
        ...


async def make_jpg_or_gif(
    img: IMG, func: Maker, gif_zoom: float = 1, gif_max_frames: int = 50
) -> BytesIO:
    """
    制作静图或者动图
    :params
      * ``img``: 输入图片，如头像
      * ``func``: 图片处理函数，输入img，返回处理后的图片
      * ``gif_zoom``: gif 图片缩放比率，避免生成的 gif 太大
      * ``direction``: gif 最大帧数，避免生成的 gif 太大
    """
    if not getattr(img, "is_animated", False):
        img = to_jpg(img).convert("RGBA")
        return save_jpg(await func(img))
    else:
        index = range(img.n_frames)
        ratio = img.n_frames / gif_max_frames
        duration = img.info["duration"] / 1000
        if ratio > 1:
            index = (int(i * ratio) for i in range(gif_max_frames))
            duration *= ratio

        frames = []
        for i in index:
            img.seek(i)
            new_img = await func(to_jpg(img).convert("RGBA"))
            frames.append(
                resize(
                    new_img,
                    (int(new_img.width * gif_zoom), int(new_img.height * gif_zoom)),
                )
            )
        return save_gif(frames, duration)


def to_image(data: bytes, allow_gif: bool = False) -> IMG:
    image = Image.open(BytesIO(data))
    if not allow_gif:
        image = to_jpg(image).convert("RGBA")
    return image


async def load_image(name: str) -> IMG:
    image = await get_image(name)
    return Image.open(BytesIO(image)).convert("RGBA")


async def load_font(name: str, fontsize: int) -> FreeTypeFont:
    font = await get_font(name)
    return ImageFont.truetype(BytesIO(font), fontsize, encoding="utf-8")


def wrap_text(text: str, font: FreeTypeFont, max_width: float, **kwargs) -> List[str]:
    line = ""
    lines = []
    for t in text:
        if t == "\n":
            lines.append(line)
            line = ""
        elif font.getsize(line + t, **kwargs)[0] > max_width:
            lines.append(line)
            line = t
        else:
            line += t
    lines.append(line)
    return lines


async def fit_font_size(
    text: str,
    max_width: float,
    max_height: float,
    fontname: str,
    max_fontsize: int,
    min_fontsize: int,
    stroke_ratio: float = 0,
) -> int:
    fontsize = max_fontsize
    while True:
        font = await load_font(fontname, fontsize)
        width, height = font.getsize_multiline(
            text, stroke_width=int(fontsize * stroke_ratio)
        )
        if width > max_width or height > max_height:
            fontsize -= 1
        else:
            return fontsize
        if fontsize < min_fontsize:
            return 0


async def translate(text: str) -> str:
    url = f"http://fanyi.youdao.com/translate"
    params = {"type": "ZH_CN2JA", "i": text, "doctype": "json"}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            result = resp.json()
        return result["translateResult"][0][0]["tgt"]
    except:
        return ""


async def help_image(commands: List[Command]) -> BytesIO:
    font = await load_font(DEFAULT_FONT, 30)
    padding = 10

    def text_img(text: str) -> IMG:
        w, h = font.getsize_multiline(text)
        img = Image.new("RGB", (w + padding * 2, h + padding * 2), "white")
        draw = ImageDraw.Draw(img)
        draw.multiline_text((padding / 2, padding / 2), text, font=font, fill="black")
        return img

    def cmd_text(cmds: List[Command], start: int = 1) -> str:
        return "\n".join(
            [f"{i + start}. " + "/".join(cmd.keywords) for i, cmd in enumerate(cmds)]
        )

    text1 = "摸头等头像相关表情制作\n触发方式：指令 + @user/qq/自己/图片\n支持的指令："
    idx = math.ceil(len(commands) / 2)
    img1 = text_img(text1)
    text2 = cmd_text(commands[:idx])
    img2 = text_img(text2)
    text3 = cmd_text(commands[idx:], start=idx + 1)
    img3 = text_img(text3)
    w = max(img1.width, img2.width + img2.width + padding)
    h = img1.height + padding + max(img2.height, img2.height)
    img = Image.new("RGB", (w + padding * 2, h + padding * 2), "white")
    img.paste(img1, (padding, padding))
    img.paste(img2, (padding, img1.height + padding))
    img.paste(img3, (img2.width + padding, img1.height + padding))
    return save_jpg(img)
