import time
import httpx
import hashlib
import imageio
from io import BytesIO
from dataclasses import dataclass
from PIL.Image import Image as IMG
from typing import Callable, List, Literal, Protocol, Tuple

from nonebot_plugin_imageutils import BuildImage

from .config import petpet_config


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

    # 没有超出最大大小，直接返回
    nbytes = output.getbuffer().nbytes
    if nbytes <= petpet_config.petpet_gif_max_size * 10**6:
        return output

    # 超出最大大小，帧数超出最大帧数时，缩减帧数
    n_frames = len(frames)
    gif_max_frames = petpet_config.petpet_gif_max_frames
    if n_frames > gif_max_frames:
        index = range(n_frames)
        ratio = n_frames / gif_max_frames
        index = (int(i * ratio) for i in range(gif_max_frames))
        new_duration = duration * ratio
        new_frames = [frames[i] for i in index]
        return save_gif(new_frames, new_duration)

    # 超出最大大小，帧数没有超出最大帧数时，缩小尺寸
    new_frames = [
        frame.resize((int(frame.width * 0.9), int(frame.height * 0.9)))
        for frame in frames
    ]
    return save_gif(new_frames, duration)


class Maker(Protocol):
    def __call__(self, img: BuildImage) -> BuildImage:
        ...


def get_avg_duration(image: IMG) -> float:
    if not getattr(image, "is_animated", False):
        return 0
    total_duration = 0
    for i in range(image.n_frames):
        image.seek(i)
        total_duration += image.info["duration"]
    return total_duration / image.n_frames


def make_jpg_or_gif(img: BuildImage, func: Maker) -> BytesIO:
    """
    制作静图或者动图
    :params
      * ``img``: 输入图片，如头像
      * ``func``: 图片处理函数，输入img，返回处理后的图片
    """
    image = img.image
    if not getattr(image, "is_animated", False):
        return func(img.convert("RGBA")).save_jpg()
    else:
        duration = get_avg_duration(image) / 1000
        frames: List[IMG] = []
        for i in range(image.n_frames):
            image.seek(i)
            frames.append(func(BuildImage(image).convert("RGBA")).image)
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
    img_duration = get_avg_duration(image) / 1000

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


async def translate(text: str, lang_from: str = "auto", lang_to: str = "zh") -> str:
    salt = str(round(time.time() * 1000))
    appid = petpet_config.baidu_trans_appid
    apikey = petpet_config.baidu_trans_apikey
    sign_raw = appid + text + salt + apikey
    sign = hashlib.md5(sign_raw.encode("utf8")).hexdigest()
    params = {
        "q": text,
        "from": lang_from,
        "to": lang_to,
        "appid": appid,
        "salt": salt,
        "sign": sign,
    }
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        result = resp.json()
    return result["trans_result"][0]["dst"]
