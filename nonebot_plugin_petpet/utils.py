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


def make_gif_or_combined_gif(
    img: BuildImage, functions: List[Maker], duration: float
) -> BytesIO:
    """
    使用静图或动图制作gif
    :params
      * ``img``: 输入图片，如头像
      * ``functions``: 图片处理函数数组，每个函数输入img并返回处理后的图片
      * ``duration``: 相邻帧之间的时间间隔，单位为秒
    """
    image = img.image
    if not getattr(image, "is_animated", False):
        img = img.convert("RGBA")
        frames: List[IMG] = []
        for func in functions:
            frames.append(func(img).image)
        return save_gif(frames, duration)

    img_frames: List[BuildImage] = []
    n_frames = image.n_frames
    img_duration = image.info["duration"] / 1000

    n_frame = 0
    time_start = 0
    for i in range(len(functions)):
        while n_frame < n_frames:
            if (
                n_frame * img_duration
                <= i * duration - time_start
                < (n_frame + 1) * img_duration
            ):
                image.seek(n_frame)
                img_frames.append(BuildImage(image).convert("RGBA"))
                print(f"add frame {n_frame}")
                break
            else:
                n_frame += 1
                if n_frame >= n_frames:
                    n_frame = 0
                    time_start += n_frames * img_duration

    frames: List[IMG] = []
    for func, img_frame in zip(functions, img_frames):
        frames.append(func(img_frame).image)
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
