from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Group
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya import Channel
from graia.ariadne.message.parser.twilight import Twilight, RegexMatch

from settings import specialqq as qq

channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage], inline_dispatchers=[Twilight([RegexMatch(r'^草+$')])]))
async def cao(app: Ariadne, group: Group):
    if group.id == qq.littleskin_cafe:
      await app.send_message(group, MessageChain(Plain('\u202e草')))

