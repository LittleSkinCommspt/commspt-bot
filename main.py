import asyncio
import sys
import traceback


from typing import List, Optional

from graia.application import GraiaMiraiApplication
from graia.application.entry import (At, Group, GroupMessage, Image,
                                     MemberJoinEvent, MessageChain, Plain)
from graia.application.message.elements import \
    Element as GraiaMessageElementType
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import FullMatch
from graia.broadcast import Broadcast
from graia.broadcast.builtin.decorators import Depend

import settings
from csllogparser import aoscPastebin
from messagepro import (MessagePro, adminOnly, exceptGroups, inGroups,
                        onCommand, onMatch, onMatchs, onWord, onWords)
from permissionshandler import PermissionsHandler
from player import PlayerProfile
from settings import specialqq as qq
from texts import TextFields as tF

from models import apis
# Application & BCC 初始化
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(broadcast=bcc, connect_info=settings.Connection)

# SimpleReplyRegister


def registerSimpleReply(command: str, reply_content: List[GraiaMessageElementType]):
    async def srr_wrapper(app: GraiaMiraiApplication, group: Group):
        await app.sendGroupMessage(group, MessageChain.create(reply_content))
    bcc.receiver(GroupMessage, dispatchers=[Kanata(
        [FullMatch(f'&{command}')])])(srr_wrapper)


registerSimpleReply('ping', [Plain('Pong!')])

registerSimpleReply('help', [Plain(tF.help)])
registerSimpleReply('manual', [
    Image.fromLocalFile('./images/rtfm.png'),
    Plain(tF.manual)
])
registerSimpleReply('faq', [
    Image.fromLocalFile('./images/rtfm.png'),
    Plain(tF.faq)
])
registerSimpleReply('ygg.server.jvm', [Plain(tF.ygg_server_jvm)])
registerSimpleReply('csl.gui', [Plain(tF.csl_gui)])
registerSimpleReply('domain', [
    Image.fromLocalFile('./images/r-search.jpg'),
    Plain(tF.domain)
])
registerSimpleReply('mail', [Plain(tF.mail)])
registerSimpleReply('csl.log', [Plain(tF.csl_log)])
registerSimpleReply('ygg.nsis', [Plain(tF.ygg_nsis)])
registerSimpleReply('browser', [
    Image.fromLocalFile('./images/browser.png'),
    Plain(tF.browser)
])
registerSimpleReply('ygg.client.refresh', [
    Image.fromLocalFile('./images/ygg-client-refresh.png'),
    Plain(tF.client_refresh)
])
registerSimpleReply('ygg.url', [
    Plain('https://littlesk.in'),
    Image.fromLocalFile('./images/ygg-url.png')
])


@bcc.receiver(MemberJoinEvent)
async def memberjoinevent_listener(app: GraiaMiraiApplication, event: MemberJoinEvent):
    member = event.member
    group = member.group
    if group.id == qq.littleskin_main:
        await app.sendGroupMessage(group, MessageChain.create(
            [At(member.id), Plain(tF.join_welcome)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([FullMatch(f'&ygg.latest')])])
async def command_ygg_latest(app: GraiaMiraiApplication, group: Group):
    infos = await apis.AuthlibInjectorLatest.get()
    _message = f'authlib-injector 最新版本：{infos.version}\n{infos.download_url}'
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([FullMatch(f'&csl.latest')])])
async def command_csl_latest(app: GraiaMiraiApplication, group: Group):
    infos = await apis.CustomSkinLoaderLatest.get()
    _message = f'''CustomSkinLoader 最新版本：{infos.version}
Forge: {infos.downloads.Forge}
Fabric: {infos.downloads.Fabric}'''
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


# @bcc.receiver(GroupMessage, headless_decorators=[Depend(onCommand('clfcsl.latest'))])
# async def command_csl_latest(app: GraiaMiraiApplication, group: Group):
#     _r = requests.get(
#         'https://csl-1258131272.cos.ap-shanghai.myqcloud.com/latest.json')
#     _j: dict = _r.json()
#     _latestVersion = _j['version']
#     _forge = _j['downloads']['Forge']
#     _message = f'''CustomSkinLoader 最新版本：{_latestVersion}
# Forge: {_forge}
# {tF.clfcsl_latest}'''
#     await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


# @bcc.receiver(GroupMessage, dispatchers=[Kanata([FullMatch(f'&csl.config')])])
# async def command_csl_config_littleskin(app: GraiaMiraiApplication, group: Group):
#     _message: str = tF.csl_config_csl_group if group.id == qq.csl_group else tF.csl_config_littleskin
#     await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


# @bcc.receiver(GroupMessage, headless_decorators=[Depend(onCommand('ot')),
#                                                  Depend(exceptGroups([qq.littleskin_cafe]))])
# async def command_ot(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
#     M = MessagePro(_gm)
#     atList: List[Optional[At]] = [At(t.target)
#                                   for t in M.at] if M.at != [] else []
#     await app.sendGroupMessage(group, MessageChain.create([
#         Image.fromLocalFile('./images/off-topic.png'),
#         *atList,
#         # 仅在 LittleSkin 主群中启用此文本消息
#         *([Plain(tF.ot)] if group.id == qq.littleskin_main else [])
#     ]))


# @bcc.receiver(GroupMessage, headless_decorators=[Depend(onCommand('view'))])
# async def command_view(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
#     M = MessagePro(_gm)
#     _textureHash = M.Command.args
#     if not _textureHash:
#         await app.sendGroupMessage(group, MessageChain.create([Plain(tF.view_no_hash_error)]))
#     elif len(_textureHash) != 64:
#         await app.sendGroupMessage(group, MessageChain.create([Plain(tF.view_hash_length_error)]))
#     else:
#         _image_message = PlayerProfile.getPreviewByHash(_textureHash)
#         if _image_message:
#             await app.sendGroupMessage(group, MessageChain.create([_image_message]))
#         else:
#             await app.sendGroupMessage(group, MessageChain.create([Plain(tF.view_not_200_error)]))


# @bcc.receiver(GroupMessage, headless_decorators=[Depend(onCommand('csl'))])
# async def command_csl(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
#     M = MessagePro(_gm)
#     _playerName = M.Command.args if M.Command.args else M.quote_plain_message
#     _player = PlayerProfile(_playerName)
#     _message = _player.getCsl()
#     await app.sendGroupMessage(group, MessageChain.create(_message))


# @bcc.receiver(GroupMessage, headless_decorators=[Depend(onCommand('ygg'))])
# async def command_ygg(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
#     M = MessagePro(_gm)
#     _playerName = M.Command.args if M.Command.args else M.quote_plain_message
#     _player = PlayerProfile(_playerName)
#     _message = _player.getYgg()
#     await app.sendGroupMessage(group, MessageChain.create(_message))


# @bcc.receiver(GroupMessage, headless_decorators=[Depend(onCommand('ban')), Depend(adminOnly)])
# async def command_ban(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
#     M = MessagePro(_gm)

#     def add() -> str:
#         _l = str()
#         for t in M.at:
#             targetP = PermissionsHandler(t.target)
#             if not targetP.isAdmin():
#                 _result = targetP.blockme()
#                 _message = f'{t.display} {tF.ban.add_succ}\n' if _result else f'{t.display} {tF.ban.add_fail}\n'
#                 _l = f'{_l}{_message}'
#         return _l.strip('\n')

#     def remove() -> str:
#         _l = str()
#         for t in M.at:
#             targetP = PermissionsHandler(t.target)
#             _result = targetP.unblockme()
#             _message = f'{t.display} {tF.ban.remove_succ}\n' if _result else f'{t.display} {tF.ban.remove_fail}\n'
#             _l = f'{_l}{_message}'
#         return _l.strip('\n')

#     if M.Command.args:
#         subCommand = M.Command.argsList[0]
#         if subCommand == 'add':
#             await app.sendGroupMessage(group, MessageChain.create([Plain(add())]))
#         if subCommand == 'remove':
#             await app.sendGroupMessage(group, MessageChain.create([Plain(remove())]))


# @bcc.receiver(GroupMessage, headless_decorators=[Depend(onWord('https://pastebin.aosc.io/paste/'))])
# async def parse_csl_log(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
#     await app.sendGroupMessage(group, MessageChain.create([Plain(tF.csl_log_parsing)]))
#     M = MessagePro(_gm)
#     fromLs = group.id in [
#         qq.littleskin_main,
#         qq.littleskin_cafe
#     ]
#     try:
#         _message = aoscPastebin(M.plain_message, fromLittleSkin=fromLs)
#         await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))
#     except Exception as e:
#         await app.sendGroupMessage(group, MessageChain.create([Plain(e)]))


# @bcc.receiver(GroupMessage, headless_decorators=[Depend(onMatch(r'^草*$')),
#                                                  Depend(exceptGroups([qq.littleskin_main, qq.csl_group]))])
# async def grass_spammer(app: GraiaMiraiApplication, group: Group):
#     await app.sendGroupMessage(group, MessageChain.create([Plain('草\u202e')]))


# @bcc.receiver(GroupMessage, headless_decorators=[Depend(onMatchs([r'^为什么.*', r'^为啥.*', r'^问个问题.*', r'^请问.*', r'^问一下.*', r'^求助一下.*', r'^如何解决.*', r'^我想问问.*', r'^这是什么问题.*', r'^这是咋回事.*', r'^怎么办.*', r'^怎么解决.*'])),
#                                                  Depend(inGroups([qq.littleskin_main]))])
# async def why_listener(app: GraiaMiraiApplication, _gm: GroupMessage):
#     M = MessagePro(_gm)
#     await app.sendGroupMessage(qq.notification_channel,
#                                MessageChain.create([Plain(tF.why_notify)]),
#                                quote=M.source)



if __name__ == '__main__':
    app.launch_blocking()

