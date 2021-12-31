from typing import Type
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler, T_State
from nonebot.adapters.cqhttp import Bot, Event, MessageEvent, GroupMessageEvent

from .data_source import commands, make_image

__help__plugin_name__ = 'petpet'
__des__ = '摸头等头像相关表情生成'
__cmd__ = '''
摸/亲/贴/顶/拍/撕/丢/爬/精神支柱/一直/加载中 {qq/@user/自己/图片}
'''.strip()
__example__ = '''
摸 @小Q
摸 114514
摸 自己
摸 [图片]
'''.strip()
__usage__ = f'{__des__}\nUsage:\n{__cmd__}\nExample:\n{__example__}'


async def handle(matcher: Type[Matcher], event: MessageEvent, type: str):
    msg = event.get_message()
    segments = []
    for msg_seg in msg:
        if msg_seg.type == 'at':
            segments.append(msg_seg.data['qq'])
        elif msg_seg.type == 'image':
            segments.append(msg_seg.data['url'])
        elif msg_seg.type == 'text':
            for text in str(msg_seg.data['text']).split():
                if text.isdigit() and len(text) >= 5:
                    segments.append(text)
                elif text == '自己':
                    segments.append(str(event.user_id))

    arg_num = commands[type].get('arg_num', 1)
    if not segments and isinstance(event, GroupMessageEvent) and event.is_tome():
        segments.append(str(event.self_id))
    if segments and len(segments) == arg_num - 1:
        segments.insert(0, str(event.user_id))

    segments = segments[:arg_num]
    if len(segments) == arg_num:
        matcher.block = True
        image = await make_image(type, segments)
        if image:
            await matcher.finish(image)
    else:
        matcher.block = False
        await matcher.finish()


def create_matchers():

    def create_handler(type: str) -> T_Handler:
        async def handler(bot: Bot, event: Event, state: T_State):
            await handle(matcher, event, type)
        return handler

    for command, params in commands.items():
        matcher = on_command(command, aliases=params['aliases'], priority=7)
        matcher.append_handler(create_handler(command))


create_matchers()
