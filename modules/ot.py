from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.element import Image, Plain
from graia.ariadne.model import Group
from graia.saya import Channel
from texts import TextFields as tF
from settings import specialqq as qq

channel = Channel.current()

# 在 commspt 群触发，发送到 littleskin_main
@channel.use(CommandSchema('&ot'))
async def ot(app: Ariadne, group: Group):
    if group.id == qq.commspt_group:
        await app.send_group_message(qq.littleskin_main, MessageChain([
            Image(path='./images/off-topic.png'),
            Plain(tF.ot)
        ]))
