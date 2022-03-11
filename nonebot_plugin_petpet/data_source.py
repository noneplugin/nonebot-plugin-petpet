from io import BytesIO
from typing import List, Union

from .download import download_url, download_avatar
from .utils import to_image
from .models import UserInfo, Command
from .functions import *

commands = [
    Command(("摸", "摸摸", "摸头", "摸摸头", "rua"), petpet, arg_num=1),
    Command(("亲", "亲亲"), kiss),
    Command(("贴", "贴贴", "蹭", "蹭蹭"), rub),
    Command(("顶", "玩"), play),
    Command(("拍",), pat),
    Command(("撕",), rip, arg_num=2),
    Command(("丢", "扔"), throw),
    Command(("抛", "掷"), throw_gif),
    Command(("爬",), crawl, arg_num=1),
    Command(("精神支柱",), support),
    Command(("一直",), always, convert=False),
    Command(("加载中",), loading, convert=False),
    Command(("转",), turn),
    Command(("小天使",), littleangel, convert=False, arg_num=1),
    Command(("不要靠近",), dont_touch),
    Command(("一样",), alike),
    Command(("滚",), roll),
    Command(("玩游戏", "来玩游戏"), play_game, convert=False, arg_num=1),
    Command(("膜", "膜拜"), worship),
    Command(("吃",), eat),
    Command(("啃",), bite),
    Command(("出警",), police),
    Command(("警察",), police1, convert=False),
    Command(("问问", "去问问"), ask, convert=False, arg_num=1),
    Command(("舔", "舔屏", "prpr"), prpr, convert=False),
    Command(("搓",), twist),
    Command(("墙纸",), wallpaper, convert=False),
    Command(("国旗",), china_flag),
    Command(("交个朋友",), make_friend, convert=False, arg_num=1),
    Command(("继续干活",), back_to_work, convert=False),
    Command(("完美", "完美的"), perfect, convert=False),
    Command(("关注",), follow, arg_num=1),
    Command(("我朋友说", "我有个朋友说"), my_friend, arg_num=2),
    Command(("这像画吗",), paint, convert=False),
    Command(("震惊",), shock),
    Command(("兑换券",), coupon, arg_num=1),
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
