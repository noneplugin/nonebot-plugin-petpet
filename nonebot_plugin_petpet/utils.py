import math
import httpx
import imageio
from io import BytesIO
from dataclasses import dataclass
from PIL.Image import Image as IMG
from typing_extensions import Literal
from typing import Callable, List, Tuple, Protocol

from nonebot.utils import run_sync
from nonebot_plugin_imageutils import BuildImage, Text2Image


@dataclass
class UserInfo:
    qq: str = ""
    group: str = ""
    name: str = ""
    gender: Literal["male", "female", "unknown"] = "unknown"
    img_url: str = ""
    img: BuildImage = BuildImage.new("RGBA", (640, 640))


@dataclass
class Command:
    func: Callable
    keywords: Tuple[str, ...]
    pattern: str = ""

    def __post_init__(self):
        if not self.pattern:
            self.pattern = "|".join(self.keywords)


def save_gif(frames: List[IMG], duration: float) -> BytesIO:
    output = BytesIO()
    imageio.mimsave(output, frames, format="gif", duration=duration)
    return output


class Maker(Protocol):
    def __call__(self, img: BuildImage) -> BuildImage:
        ...


def make_jpg_or_gif(
    img: BuildImage, func: Maker, gif_zoom: float = 1, gif_max_frames: int = 50
) -> BytesIO:
    """
    制作静图或者动图
    :params
      * ``img``: 输入图片，如头像
      * ``func``: 图片处理函数，输入img，返回处理后的图片
      * ``gif_zoom``: gif 图片缩放比率，避免生成的 gif 太大
      * ``gif_max_frames``: gif 最大帧数，避免生成的 gif 太大
    """
    image = img.image
    if not getattr(image, "is_animated", False):
        return func(img.convert("RGBA")).save_jpg()
    else:
        index = range(image.n_frames)
        ratio = image.n_frames / gif_max_frames
        duration = image.info["duration"] / 1000
        if ratio > 1:
            index = (int(i * ratio) for i in range(gif_max_frames))
            duration *= ratio

        frames = []
        for i in index:
            image.seek(i)
            new_img = func(BuildImage(image).convert("RGBA"))
            frames.append(
                new_img.resize(
                    (int(new_img.width * gif_zoom), int(new_img.height * gif_zoom))
                ).image
            )
        return save_gif(frames, duration)


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


@run_sync
def help_image(commands: List[Command]) -> BytesIO:
    def cmd_text(cmds: List[Command], start: int = 1) -> str:
        return "\n".join(
            [f"{i + start}. " + "/".join(cmd.keywords) for i, cmd in enumerate(cmds)]
        )

    text1 = "摸头等头像相关表情制作\n触发方式：指令 + @某人 / qq号 / 自己 / [图片]\n支持的指令："
    idx = math.ceil(len(commands) / 2)
    text2 = cmd_text(commands[:idx])
    text3 = cmd_text(commands[idx:], start=idx + 1)
    img1 = Text2Image.from_text(text1, 30, weight="bold").to_image(padding=(20, 10))
    img2 = Text2Image.from_text(text2, 30).to_image(padding=(20, 10))
    img3 = Text2Image.from_text(text3, 30).to_image(padding=(20, 10))
    w = max(img1.width, img2.width + img3.width)
    h = img1.height + max(img2.height, img2.height)
    img = BuildImage.new("RGBA", (w, h), "white")
    img.paste(img1, alpha=True)
    img.paste(img2, (0, img1.height), alpha=True)
    img.paste(img3, (img2.width, img1.height), alpha=True)
    return img.save_jpg()
