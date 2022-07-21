from io import BytesIO
from typing import Union

from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.plugin import PluginMetadata
from nonebot import on_command, require, on_message
from nonebot.adapters.onebot.v11 import MessageSegment

require("nonebot_plugin_imageutils")

from .data_source import commands
from .depends import split_msg, regex
from .utils import Command, help_image

__plugin_meta__ = PluginMetadata(
    name="头像表情包",
    description="摸头等头像相关表情制作",
    usage="触发方式：指令 + @user/qq/自己/图片\n发送“头像表情包”查看支持的指令",
    extra={
        "unique_name": "petpet",
        "example": "摸 @小Q\n摸 114514\n摸 自己\n摸 [图片]",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.3.7",
    },
)


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
            matcher.stop_propagation()
            if isinstance(res, str):
                await matcher.finish(res)
            await matcher.finish(MessageSegment.image(res))

        return handle

    for command in commands:
        on_message(
            regex(command.pattern),
            block=False,
            priority=12,
        ).append_handler(handler(command), parameterless=[split_msg()])


create_matchers()
