from typing import List, Union

from .download import download_url, download_avatar
from .utils import to_image
from .functions import *


commands = {
    'petpet': {
        'aliases': {'摸', '摸摸', 'rua'},
        'func': petpet
    },
    'kiss': {
        'aliases': {'亲', '亲亲'},
        'func': kiss,
        'arg_num': 2
    },
    'rub': {
        'aliases': {'贴', '贴贴', '蹭', '蹭蹭'},
        'func': rub,
        'arg_num': 2
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
        'convert': False
    },
    'dont_touch': {
        'aliases': {'不要靠近'},
        'func': dont_touch
    },
    'alike': {
        'aliases': {'一样'},
        'func': alike
    }
}


async def make_image(type: str, segments: List[str], name: str = '') -> Union[str, BytesIO]:
    convert = commands[type].get('convert', True)
    func = commands[type]['func']

    images = []
    for s in segments:
        if s.isdigit():
            images.append(await download_avatar(s))
        else:
            images.append(await download_url(s))

    images = [to_image(i, convert) for i in images]
    return await func(*images, name=name)
