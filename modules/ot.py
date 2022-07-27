from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.element import Image, Plain
from graia.ariadne.model import Group
from graia.saya import Channel
from texts import TextFields as tF
from settings import specialqq as qq

channel = Channel.current()


@channel.use(CommandSchema('&ot'))
async def ot(app: Ariadne, group: Group):
    if group.id == qq.littleskin_main or group.id == qq.csl_group:
        await app.send_message(group, MessageChain([
            Image(path='./images/off-topic.png'),
            Plain(tF.ot)
        ]))
