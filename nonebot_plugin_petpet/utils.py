import httpx
import imageio
from io import BytesIO
from dataclasses import dataclass
from PIL.Image import Image as IMG
from typing_extensions import Literal
from typing import Callable, List, Tuple, Protocol

from nonebot_plugin_imageutils import BuildImage


@dataclass
class UserInfo:
    qq: str = ""
    group: str = ""
    name: str = ""
    gender: Literal["male", "female", "unknown"] = "unknown"
    img_url: str = ""
    img: BuildImage = BuildImage.new("RGBA", (640, 640))


@dataclass
class Meme:
    name: str
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

        frames: List[IMG] = []
        for i in index:
            image.seek(i)
            new_img = func(BuildImage(image).convert("RGBA"))
            new_img = new_img.resize(
                (int(new_img.width * gif_zoom), int(new_img.height * gif_zoom))
            )
            bg = BuildImage.new("RGBA", new_img.size, "white")
            bg.paste(new_img, alpha=True)
            frames.append(bg.image)
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
