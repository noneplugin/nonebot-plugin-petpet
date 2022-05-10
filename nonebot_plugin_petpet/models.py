from io import BytesIO
from PIL import Image
from PIL.Image import Image as IMG
from dataclasses import dataclass
from typing import List, Tuple, Protocol


class UserInfo:
    def __init__(self, qq: str = "", group: str = "", img_url: str = ""):
        self.qq: str = qq
        self.group: str = group
        self.name: str = ""
        self.gender: str = ""  # male 或 female 或 unknown
        self.img_url: str = img_url
        self.img: IMG = Image.new("RGBA", (640, 640))


class Func(Protocol):
    async def __call__(self, users: List[UserInfo], **kwargs) -> BytesIO:
        ...


@dataclass
class Command:
    keywords: Tuple[str, ...]
    func: Func
    allow_gif: bool = False
    arg_num: int = 0
