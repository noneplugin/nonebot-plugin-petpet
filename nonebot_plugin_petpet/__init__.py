import traceback
from typing import List, Type
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageSegment,
    MessageEvent,
    GroupMessageEvent,
)
from nonebot.log import logger

from .data_source import commands, make_image
from .download import DownloadError, ResourceError
from .utils import text_to_pic
from .models import UserInfo


__help__plugin_name__ = "petpet"
__des__ = "摸头等头像相关表情制作"
petpet_help = [
    f"{i}. {'/'.join(list(c['aliases']))}"
    for i, c in enumerate(commands.values(), start=1)
]
petpet_help = "\n".join(petpet_help)
__cmd__ = f"""
触发方式：指令 + @user/qq/自己/图片
支持的指令：
{petpet_help}
""".strip()
__example__ = """
摸 @小Q
摸 114514
摸 自己
摸 [图片]
""".strip()
__usage__ = f"{__des__}\n\nUsage:\n{__cmd__}\n\nExamples:\n{__example__}"


help_cmd = on_command("头像表情包", aliases={"头像相关表情包", "头像相关表情制作"}, block=True, priority=12)


@help_cmd.handle()
async def _():
    img = await text_to_pic(__usage__)
    if img:
        await help_cmd.finish(MessageSegment.image(img))


def is_qq(msg: str):
    return msg.isdigit() and 11 >= len(msg) >= 5


async def get_user_info(bot: Bot, user: UserInfo):
    if not user.qq:
        return

    if user.group:
        info = await bot.get_group_member_info(
            group_id=int(user.group), user_id=int(user.qq)
        )
        user.name = info.get("card", "") or info.get("nickname", "")
        user.gender = info.get("sex", "")
    else:
        info = await bot.get_stranger_info(user_id=int(user.qq))
        user.name = info.get("nickname", "")
        user.gender = info.get("sex", "")


async def handle(
    matcher: Type[Matcher], bot: Bot, event: MessageEvent, type: str, msg: Message
):
    users: List[UserInfo] = []
    sender: UserInfo = UserInfo(qq=str(event.user_id))
    args: List[str] = []

    for msg_seg in msg:
        if msg_seg.type == "at":
            users.append(
                UserInfo(
                    qq=msg_seg.data["qq"],
                    group=str(event.group_id)
                    if isinstance(event, GroupMessageEvent)
                    else "",
                )
            )
        elif msg_seg.type == "image":
            users.append(UserInfo(img_url=msg_seg.data["url"]))
        elif msg_seg.type == "text":
            for text in str(msg_seg.data["text"]).split():
                if is_qq(text):
                    users.append(UserInfo(qq=text))
                elif text == "自己":
                    users.append(
                        UserInfo(
                            qq=str(event.user_id),
                            group=str(event.group_id)
                            if isinstance(event, GroupMessageEvent)
                            else "",
                        )
                    )
                else:
                    args.append(text)

    arg_num = commands[type].get("arg_num", 0)
    if len(args) > arg_num:
        matcher.block = False
        await matcher.finish()

    if not users and isinstance(event, GroupMessageEvent) and event.is_tome():
        users.append(UserInfo(qq=str(event.self_id), group=str(event.group_id)))
    if not users:
        matcher.block = False
        await matcher.finish()

    matcher.block = True

    await get_user_info(bot, sender)
    for user in users:
        await get_user_info(bot, user)

    try:
        res = await make_image(type, sender, users, args=args)
    except DownloadError:
        await matcher.finish("图片下载出错，请稍后再试")
    except ResourceError:
        await matcher.finish("资源下载出错，请稍后再试")
    except:
        logger.warning(traceback.format_exc())
        await matcher.finish("出错了，请稍后再试")

    if not res:
        await matcher.finish("出错了，请稍后再试")
    if isinstance(msg, str):
        await matcher.finish(msg)
    else:
        await matcher.finish(MessageSegment.image(res))


def create_matchers():
    def create_handler(type: str) -> T_Handler:
        async def handler(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
            await handle(matcher, bot, event, type, msg)

        return handler

    for command, params in commands.items():
        matcher = on_command(
            command, aliases=params["aliases"], block=True, priority=12
        )
        matcher.append_handler(create_handler(command))


create_matchers()
