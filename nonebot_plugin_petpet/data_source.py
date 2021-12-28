from typing import List
from nonebot.log import logger
from nonebot.adapters.cqhttp import MessageSegment

from .download import download_image, DownloadError
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
    }
}


async def make_image(type: str, images: List[str]):
    try:
        if type not in commands:
            return None

        convert = commands[type].get('convert', True)
        func = commands[type]['func']
        images = [load_image(await download_image(i), convert) for i in images]
        result = await func(*images)
        return MessageSegment.image(result)

    except DownloadError:
        return '下载出错，请稍后再试'
    except Exception as e:
        logger.warning(
            f"Error in make_image({type}, [{', '.join(images)}]): {e}")
        return '出错了，请稍后再试'
