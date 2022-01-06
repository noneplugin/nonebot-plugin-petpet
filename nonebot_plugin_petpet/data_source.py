from typing import List, Union

from .download import download_url, download_avatar
from .utils import to_image
from .models import UserInfo
from .functions import *


commands = {
    'petpet': {
        'aliases': {'摸', '摸摸', 'rua'},
        'func': petpet
    },
    'kiss': {
        'aliases': {'亲', '亲亲'},
        'func': kiss
    },
    'rub': {
        'aliases': {'贴', '贴贴', '蹭', '蹭蹭'},
        'func': rub
    },
    'play': {
        'aliases': {'顶', '玩'},
        'func': play
    },
    'pat': {
        'aliases': {'拍'},
        'func': pat
    },
    'rip': {
        'aliases': {'撕'},
        'func': rip
    },
    'throw': {
        'aliases': {'丢', '扔'},
        'func': throw
    },
    'crawl': {
        'aliases': {'爬'},
        'func': crawl
    },
    'support': {
        'aliases': {'精神支柱'},
        'func': support
    },
    'always': {
        'aliases': {'一直'},
        'func': always,
        'convert': False
    },
    'loading': {
        'aliases': {'加载中'},
        'func': loading,
        'convert': False
    },
    'turn': {
        'aliases': {'转'},
        'func': turn
    },
    'littleangel': {
        'aliases': {'小天使'},
        'func': littleangel,
        'convert': False,
        'arg_num': 1
    },
    'dont_touch': {
        'aliases': {'不要靠近'},
        'func': dont_touch
    },
    'alike': {
        'aliases': {'一样'},
        'func': alike
    },
    'roll': {
        'aliases': {'滚'},
        'func': roll
    },
    'play_game': {
        'aliases': {'玩游戏', '来玩游戏'},
        'func': play_game,
        'convert': False
    }
}


async def download_image(user: UserInfo, convert: bool = True):
    if user.qq:
        user.img = await download_avatar(user.qq)
    elif user.img_url:
        user.img = await download_url(user.img_url)

    if user.img:
        user.img = to_image(user.img, convert)


async def make_image(type: str, sender: UserInfo, users: List[UserInfo], args: List[str] = []) -> Union[str, BytesIO]:
    convert = commands[type].get('convert', True)
    func = commands[type]['func']

    await download_image(sender, convert)
    for user in users:
        await download_image(user, convert)

    return await func(users, sender=sender, args=args)
