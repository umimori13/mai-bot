import random
import re

from PIL import Image
from nonebot import on_command, on_message, on_notice, require, get_driver, on_regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Message, Event, Bot
from src.libraries.image import *
from random import randint

import time
from collections import defaultdict

# help = on_command('help')


# @help.handle()
# async def _(bot: Bot, event: Event, state: T_State):
#     help_str = '''可用命令如下：
# 今日舞萌 查看今天的舞萌运势
# XXXmaimaiXXX什么 随机一首歌
# 随个[dx/标准][绿黄红紫白]<难度> 随机一首指定条件的乐曲
# 查歌<乐曲标题的一部分> 查询符合条件的乐曲
# [绿黄红紫白]id<歌曲编号> 查询乐曲信息或谱面信息
# <歌曲别名>是什么歌 查询乐曲别名对应的乐曲
# 定数查歌 <定数>  查询定数对应的乐曲
# 定数查歌 <定数下限> <定数上限>
# 分数线 <难度+歌曲id> <分数线> 详情请输入“分数线 帮助”查看'''
#     await help.send(Message([{
#         "type": "image",
#         "data": {
#             "file": f"base64://{str(image_to_base64(text_to_image(help_str)), encoding='utf-8')}"
#         }
#     }]))


#帮助功能
help = on_command('help')

@help.handle()
async def _(bot: Bot, event: Event, state: T_State):
    v = str(event.get_message()).strip()
    help_text: dict = get_driver().config.help_text
    if v == "":
        help_str = '\n'.join([f'.help {key}\t{help_text[key][0]}' for key in help_text])
        await help.finish(help_str)
    else:
        await help.finish(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(text_to_image(help_text[v][1])), encoding='utf-8')}"
            }
        }]))


async def _group_poke(bot: Bot, event: Event, state: dict) -> bool:
    value = (event.notice_type == "notify" and event.sub_type == "poke" and event.target_id == int(bot.self_id))
    return value


#戳一戳功能
poke = on_notice(rule=_group_poke, priority=10, block=True)
poke_dict = defaultdict(lambda: defaultdict(int))

@poke.handle()
async def _(bot: Bot, event: Event, state: T_State):
    v = "default"
    if event.__getattribute__('group_id') is None:
        event.__delattr__('group_id')
    else:
        group_dict = poke_dict[event.__getattribute__('group_id')]
        group_dict[event.sender_id] += 1
        # v = await invoke_poke(event.group_id, event.sender_id)
        # if v == "disabled":
        #     await poke.finish()
        #     return
    r = randint(1, 20)
    time.sleep(1)
    if v == "limited":
        await poke.send(Message([{
            "type": "poke",
            "data": {
                "qq": f"{event.sender_id}"
            }
        }]))
    elif r == 2:
        await poke.send(Message('不许戳'))
    # elif r == 3:
    #     url = await get_jlpx('戳', '呜呜w', '闲着没事干')
    #     await poke.send(Message([{
    #         "type": "image",
    #         "data": {
    #             "file": url
    #         }
    #     }]))
    elif r == 4:
        img_p = Image.open(path)
        draw_text(img_p, '戳', 0)
        draw_text(img_p, '有尝试过玩Cytus II吗', 400)
        await poke.send(Message([{
            "type": "image",
            "data": {
                "file": f"base64://{str(image_to_base64(img_p), encoding='utf-8')}"
            }
        }]))
    elif r == 5:
        await poke.send(Message('呜呜呜再戳人家要哭哭了啦'))
    elif r <= 7:
        await poke.send(Message([{
            "type": "image",
            "data": {
                "file": f"https://www.diving-fish.com/images/poke/{r - 5}.gif",
            }
        }]))
    elif r <= 12:
        await poke.send(Message([{
            "type": "image",
            "data": {
                "file": f"https://www.diving-fish.com/images/poke/{r - 7}.jpg",
            }
        }]))
    elif r == 1:
        await poke.send(Message('喵喵喵'))
    elif r == 13:
        await poke.send(Message('哭哭'))
    elif r <=16:
         await poke.send(Message('呜！'))
    else:
        await poke.send(Message([{
            "type": "poke",
            "data": {
                "qq": f"{event.sender_id}"
            }
        }]))


#复读功能
# repeat = on_message(priority=99)

# @repeat.handle()
# async def _(bot: Bot, event: Event, state: T_State):
#     r = random.random()
#     if r <= 0.0114514:
#         await repeat.finish(event.get_message())