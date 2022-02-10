from typing import List, Union

from .download import download_url, download_avatar
from .utils import to_image
from .models import UserInfo
from .functions import *


commands = {
    "_petpet": {"aliases": {"摸", "摸摸", "rua"}, "func": petpet},
    "_kiss": {"aliases": {"亲", "亲亲"}, "func": kiss},
    "_rub": {"aliases": {"贴", "贴贴", "蹭", "蹭蹭"}, "func": rub},
    "_play": {"aliases": {"顶", "玩"}, "func": play},
    "_pat": {"aliases": {"拍"}, "func": pat},
    "_rip": {"aliases": {"撕"}, "func": rip},
    "_throw": {"aliases": {"丢", "扔"}, "func": throw},
    "_crawl": {"aliases": {"爬"}, "func": crawl},
    "_support": {"aliases": {"精神支柱"}, "func": support},
    "_always": {"aliases": {"一直"}, "func": always, "convert": False},
    "_loading": {"aliases": {"加载中"}, "func": loading, "convert": False},
    "_turn": {"aliases": {"转"}, "func": turn},
    "_littleangel": {
        "aliases": {"小天使"},
        "func": littleangel,
        "convert": False,
        "arg_num": 1,
    },
    "_dont_touch": {"aliases": {"不要靠近"}, "func": dont_touch},
    "_alike": {"aliases": {"一样"}, "func": alike},
    "_roll": {"aliases": {"滚"}, "func": roll},
    "_play_game": {"aliases": {"玩游戏", "来玩游戏"}, "func": play_game, "convert": False},
    "_worship": {"aliases": {"膜", "膜拜"}, "func": worship},
}


async def download_image(user: UserInfo, convert: bool = True):
    img = None
    if user.qq:
        img = await download_avatar(user.qq)
    elif user.img_url:
        img = await download_url(user.img_url)

    if img:
        user.img = to_image(img, convert)


async def make_image(
    type: str, sender: UserInfo, users: List[UserInfo], args: List[str] = []
) -> Union[str, BytesIO]:
    convert = commands[type].get("convert", True)
    func = commands[type]["func"]

    await download_image(sender, convert)
    for user in users:
        await download_image(user, convert)

    return await func(users, sender=sender, args=args)
