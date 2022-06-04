from io import BytesIO
from typing import Union

from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot import on_command, require, on_message
from nonebot.adapters.onebot.v11 import MessageSegment

require("nonebot_plugin_imageutils")

from .data_source import commands
from .depends import split_msg, regex
from .utils import Command, help_image

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


def create_matchers():
    def handler(command: Command) -> T_Handler:
        async def handle(
            matcher: Matcher, res: Union[str, BytesIO] = Depends(command.func)
        ):
            if isinstance(res, str):
                await matcher.finish(res)
            await matcher.finish(MessageSegment.image(res))

        return handle

    for command in commands:
        on_message(
            regex(command.pattern),
            block=True,
            priority=12,
        ).append_handler(handler(command), parameterless=[split_msg()])


create_matchers()
