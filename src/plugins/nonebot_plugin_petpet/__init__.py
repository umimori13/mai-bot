from typing import Type
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler, T_State
from nonebot.adapters.cqhttp import Bot, Event, MessageEvent

from .data_source import commands, make_image

__help__plugin_name__ = 'petpet'
__des__ = '摸头等头像相关表情生成'
__cmd__ = '''
摸/亲/贴/顶/拍/撕/丢/爬/精神支柱/一直 {qq/@user/自己/图片}
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
    images = []
    for msg_seg in msg:
        if msg_seg.type == 'at':
            images.append(msg_seg.data['qq'])
        elif msg_seg.type == 'image':
            images.append(msg_seg.data['url'])
        elif msg_seg.type == 'text':
            for text in str(msg_seg.data['text']).split():
                if text.isdigit():
                    images.append(text)
                elif text == '自己':
                    images.append(str(event.user_id))

    if not images:
        if event.is_tome():
            images.append(str(event.self_id))

    if not images:
        matcher.block = False
        await matcher.finish()

    if type in ['kiss', 'rub']:
        if len(images) < 2:
            images.insert(0, str(event.user_id))

    matcher.block = True
    image = await make_image(type, images)
    if image:
        await matcher.finish(image)


def create_matchers():

    def create_handler(type: str) -> T_Handler:
        async def handler(bot: Bot, event: Event, state: T_State):
            await handle(matcher, event, type)
        return handler

    for command, params in commands.items():
        matcher = on_command(command, aliases=params['aliases'], priority=7)
        matcher.append_handler(create_handler(command))


create_matchers()
