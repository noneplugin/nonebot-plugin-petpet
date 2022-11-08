import math
import time
import httpx
import hashlib
from enum import Enum
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
    frames[0].save(
        output,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=duration * 1000,
        loop=0,
        disposal=2,
    )

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


class GifMaker(Protocol):
    def __call__(self, i: int) -> Maker:
        ...


def get_avg_duration(image: IMG) -> float:
    if not getattr(image, "is_animated", False):
        return 0
    total_duration = 0
    for i in range(image.n_frames):
        image.seek(i)
        total_duration += image.info["duration"]
    return total_duration / image.n_frames


def make_jpg_or_gif(
    img: BuildImage, func: Maker, keep_transparency: bool = False
) -> BytesIO:
    """
    制作静图或者动图
    :params
      * ``img``: 输入图片，如头像
      * ``func``: 图片处理函数，输入img，返回处理后的图片
      * ``keep_transparency``: 传入gif时，是否保留该gif的透明度
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
        if keep_transparency:
            image.seek(0)
            frames[0].info["transparency"] = image.info.get("transparency", 0)
        return save_gif(frames, duration)


class FrameAlignPolicy(Enum):
    """
    输入gif长度大于目标gif时，是否延长目标gif长度以对齐两个gif
    """

    no_extend = 0
    """不延长"""
    extend_first = 1
    """延长第一帧"""
    extend_last = 2
    """延长最后一帧"""
    extend_loop = 3
    """以循环方式延长"""


def make_gif_or_combined_gif(
    img: BuildImage,
    maker: GifMaker,
    frame_num: int,
    duration: float,
    frame_align: FrameAlignPolicy = FrameAlignPolicy.no_extend,
) -> BytesIO:
    """
    使用静图或动图制作gif
    :params
      * ``img``: 输入图片，如头像
      * ``maker``: 图片处理函数生成，传入第几帧，返回对应的图片处理函数
      * ``frame_num``: 目标gif的帧数
      * ``duration``: 相邻帧之间的时间间隔，单位为秒
      * ``frame_align``: 输入gif长度大于目标gif时，gif长度对齐方式
    """
    image = img.image
    if not getattr(image, "is_animated", False):
        img = img.convert("RGBA")
        return save_gif([maker(i)(img).image for i in range(frame_num)], duration)

    frame_num_in = image.n_frames
    duration_in = get_avg_duration(image) / 1000
    total_duration_in = frame_num_in * duration_in
    total_duration = frame_num * duration

    func_idxs: List[int] = list(range(frame_num))
    diff_duration = total_duration_in - total_duration
    diff_num = int((total_duration_in - total_duration) / duration)

    if diff_duration >= duration:
        if frame_align == FrameAlignPolicy.extend_first:
            func_idxs = [0] * diff_num + func_idxs

        elif frame_align == FrameAlignPolicy.extend_last:
            func_idxs = func_idxs + [frame_num - 1] * diff_num

        elif frame_align == FrameAlignPolicy.extend_loop:
            frame_num_total = frame_num
            while frame_num_total + frame_num <= petpet_config.petpet_gif_max_frames:
                frame_num_total += frame_num
                func_idxs += list(range(frame_num))
                multiple = round(frame_num_total * duration / total_duration_in)
                if (
                    math.fabs(total_duration_in * multiple - frame_num_total * duration)
                    <= duration
                ):
                    break

    frames: List[IMG] = []
    frame_idx_in = 0
    time_start = 0
    for i, idx in enumerate(func_idxs):
        func = maker(idx)
        while frame_idx_in < frame_num_in:
            if (
                frame_idx_in * duration_in
                <= i * duration - time_start
                < (frame_idx_in + 1) * duration_in
            ):
                image.seek(frame_idx_in)
                frame = func(BuildImage(image).convert("RGBA"))
                frames.append(frame.image)
                break
            else:
                frame_idx_in += 1
                if frame_idx_in >= frame_num_in:
                    frame_idx_in = 0
                    time_start += frame_num_in * duration_in

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
