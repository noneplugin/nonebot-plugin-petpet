import shlex
import traceback
from typing import List, Type
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler, T_RuleChecker, T_State
from nonebot.params import CommandArg, State
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageSegment,
    MessageEvent,
    GroupMessageEvent,
)
from nonebot.log import logger

from .data_source import make_image, commands
from .download import DownloadError, ResourceError
from .utils import help_image
from .models import UserInfo, Command


__help__plugin_name__ = "petpet"
__des__ = "摸头等头像相关表情制作"
__cmd__ = f"""
触发方式：指令 + @user/qq/自己/图片
发送“头像表情包”查看支持的指令
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
    img = await help_image(commands)
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


def check_args_rule(command: Command) -> T_RuleChecker:
    async def check_args(
        bot: Bot,
        event: MessageEvent,
        state: T_State = State(),
        msg: Message = CommandArg(),
    ) -> bool:

        users: List[UserInfo] = []
        args: List[str] = []

        if event.reply:
            reply_imgs = event.reply.message["image"]
            for reply_img in reply_imgs:
                users.append(UserInfo(img_url=reply_img.data["url"]))

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
                raw_text = str(msg_seg)
                try:
                    texts = shlex.split(raw_text)
                except:
                    texts = raw_text.split()
                for text in texts:
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
                        text = text.strip()
                        if text:
                            args.append(text)

        if len(args) > command.arg_num:
            return False
        if not users and isinstance(event, GroupMessageEvent) and event.is_tome():
            users.append(UserInfo(qq=str(event.self_id), group=str(event.group_id)))
        if not users:
            return False

        sender = UserInfo(qq=str(event.user_id))
        await get_user_info(bot, sender)
        for user in users:
            await get_user_info(bot, user)
        state["sender"] = sender
        state["users"] = users
        state["args"] = args
        return True

    return check_args


async def handle(
    matcher: Type[Matcher],
    command: Command,
    sender: UserInfo,
    users: List[UserInfo],
    args: List[str],
):
    try:
        res = await make_image(command, sender, users, args=args)
    except DownloadError:
        await matcher.finish("图片下载出错，请稍后再试")
    except ResourceError:
        await matcher.finish("资源下载出错，请稍后再试")
    except:
        logger.warning(traceback.format_exc())
        await matcher.finish("出错了，请稍后再试")

    if not res:
        await matcher.finish("出错了，请稍后再试")
    if isinstance(res, str):
        await matcher.finish(res)
    else:
        await matcher.finish(MessageSegment.image(res))


def create_matchers():
    def create_handler(command: Command) -> T_Handler:
        async def handler(state: T_State = State()):
            await handle(
                matcher, command, state["sender"], state["users"], state["args"]
            )

        return handler

    for command in commands:
        matcher = on_command(
            command.keywords[0],
            aliases=set(command.keywords),
            rule=check_args_rule(command),
            block=True,
            priority=12,
        )
        matcher.append_handler(create_handler(command))


create_matchers()
