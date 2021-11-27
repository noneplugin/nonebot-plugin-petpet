from typing import Type
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters.cqhttp import Bot, Event, MessageEvent

from .data_source import commands, make_image

__usage__ = """
头像相关表情生成
Usage:\n  摸/亲/贴/顶/撕/丢/爬/精神支柱 {qq/@user/自己/图片}
"""


async def handle(matcher: Type[Matcher], event: MessageEvent, type: str):
    msg = event.get_message()
    msg_text = event.get_plaintext().strip()
    self_id = event.user_id
    user_id = ''
    img_url = ''

    for msg_seg in msg:
        if msg_seg.type == 'at':
            user_id = msg_seg.data['qq']
            break
        elif msg_seg.type == 'image':
            img_url = msg_seg.data['url']
            break

    if not (user_id or img_url):
        if msg_text.isdigit():
            user_id = msg_text
        elif msg_text == '自己':
            user_id = event.user_id
        else:
            matcher.block = False
            await matcher.finish()

    matcher.block = True
    image = await make_image(type, self_id, user_id=user_id, img_url=img_url)
    if image:
        await matcher.finish(image)


matcher_tpl = """
{command} = on_command('{command}', aliases={aliases}, priority=7)

@{command}.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await handle({command}, event, '{command}')
"""

for command, params in commands.items():
    exec(matcher_tpl.format(command=command, aliases=params['aliases']))
