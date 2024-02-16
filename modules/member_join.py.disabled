from graia.ariadne.app import Ariadne
from graia.ariadne.event.mirai import MemberJoinEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Plain
from graia.ariadne.model import Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from settings import specialqq as qq
from texts import TextFields as tF
from utils.db_manager import get_uid

channel = Channel.current()

@channel.use(ListenerSchema([MemberJoinEvent]))
async def memberjoinevent_listener(app: Ariadne, group: Group, member: Member):
    if group.id == qq.littleskin_main:
        await app.send_message(group, MessageChain(
            [At(member.id), Plain(f' $UID{await get_uid(member.id)}  '), Plain(tF.join_welcome)]))

