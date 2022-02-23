from io import BytesIO
from typing import List, Union

from .download import download_url, download_avatar
from .utils import to_image
from .models import UserInfo, Command
from .functions import *

commands = [
    Command(("摸", "摸摸", "rua"), petpet),
    Command(("亲", "亲亲"), kiss),
    Command(("贴", "贴贴", "蹭", "蹭蹭"), rub),
    Command(("顶", "玩"), play),
    Command(("拍",), pat),
    Command(("撕",), rip),
    Command(("丢", "扔"), throw),
    Command(("爬",), crawl),
    Command(("精神支柱",), support),
    Command(("一直",), always, convert=False),
    Command(("加载中",), loading, convert=False),
    Command(("转",), turn),
    Command(("小天使",), littleangel, convert=False, arg_num=1),
    Command(("不要靠近",), dont_touch),
    Command(("一样",), alike),
    Command(("滚",), roll),
    Command(("玩游戏", "来玩游戏"), play_game, convert=False),
    Command(("膜", "膜拜"), worship),
    Command(("吃",), eat),
    Command(("啃",), bite),
    Command(("出警",), police),
    Command(("问问", "去问问"), ask, convert=False, arg_num=1),
]


async def download_image(user: UserInfo, convert: bool = True):
    img = None
    if user.qq:
        img = await download_avatar(user.qq)
    elif user.img_url:
        img = await download_url(user.img_url)

    if img:
        user.img = to_image(img, convert)


async def make_image(
    command: Command, sender: UserInfo, users: List[UserInfo], args: List[str] = []
) -> Union[str, BytesIO]:
    await download_image(sender, command.convert)
    for user in users:
        await download_image(user, command.convert)
    return await command.func(users, sender=sender, args=args)
