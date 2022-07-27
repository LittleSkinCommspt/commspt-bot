from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.element import Plain, Source
from graia.ariadne.model import Group, Member
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya import Channel
from graia.ariadne.message.parser.twilight import Twilight, RegexMatch
from utils.matchers import KeywordsMatch
from texts import TextFields as tF
from settings import specialqq as qq

channel = Channel.current()


@channel.use(ListenerSchema([GroupMessage], inline_dispatchers=[Twilight([KeywordsMatch(tF.question_keywords)])]))
async def ask(app: Ariadne, group: Group, member: Member, msg: MessageChain):
    if group.id in [qq.littleskin_main]:
        for i in tF.question_keywords_excepted:
            if i in msg.safe_display:
                return
        admins = await app.get_member_list(qq.notification_channel)
        admins_id = [m.id for m in admins]
        if member.id not in admins_id:
            await app.send_group_message(qq.notification_channel,
                                   MessageChain(
                                       [Plain(tF.new_question_nofication)]),
                                   quote=msg[Source][0])
            await app.send_message(group,
                                   MessageChain(
                                       [Plain(tF.new_question_sent)]),
                                   quote=msg[Source][0].id)


# @channel.use(ListenerSchema([GroupMessage], inline_dispatchers=[Twilight([RegexMatch(r'^草+$')])]))


# @broadcast.receiver(GroupMessage, dispatchers=[
#     Twilight(Sparkle([KeywordsMatch(tF.question_keywords)]))
# ])
# async def new_question_nofication(app: Ariadne, group: Group, member: Member, msg: MessageChain):
#     for i in tF.question_keywords_excepted:
#         if i in msg.safe_display():
#             return
#     enable_in_groups: List[int] = [qq.littleskin_main]
#     admins = await app.getMemberList(qq.notification_channel)
#     admins_id = [m.id for m in admins]
#     if group.id in enable_in_groups and member.id not in admins_id:
#         await app.sendGroupMessage(qq.notification_channel,
#                                     MessageChain(
#                                         [Plain(tF.new_question_nofication)]),
#                                     quote=msg[Source][0].id)
#         await app.sendGroupMessage(group,
#                                     MessageChain(
#                                         [Plain(tF.new_question_sent)]),
#                                     quote=msg[Source][0].id)
