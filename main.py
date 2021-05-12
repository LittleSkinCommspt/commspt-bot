import asyncio
from typing import List
from uuid import UUID

from graia.application import GraiaMiraiApplication
from graia.application.entry import (At, Group, GroupMessage, Image, Source,
                                     MemberJoinEvent, MessageChain, Plain,
                                     Quote)
from graia.application.message.elements import \
    Element as GraiaMessageElementType
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import (FullMatch,
                                                        OptionalParam,
                                                        RegexMatch,
                                                        RequireParam)
from graia.broadcast import Broadcast

import settings
from models import apis
from settings import specialqq as qq
from texts import TextFields as tF

# Application & BCC 初始化
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc, connect_info=settings.Connection, enable_chat_log=False)


def MatchCommand(command: str):
    return RegexMatch(rf'(.*: )?&{command} *')  # 兼容 Constance


def MatchKeywords(keywords: list):  # 仅适用于非最后一个关键词
    return [Kanata([RegexMatch(f'.*{i}.*')], stop_exec_if_fail=False) for i in keywords]


def SimpleReply(command: str, reply_content: List[GraiaMessageElementType]):
    async def srr_wrapper(app: GraiaMiraiApplication, group: Group):
        await app.sendGroupMessage(group, MessageChain.create(reply_content))
    bcc.receiver(GroupMessage, dispatchers=[Kanata(
        [MatchCommand(command)])])(srr_wrapper)


SimpleReply('ping', [Plain('Pong!')])

SimpleReply('help', [Plain(tF.help)])
SimpleReply('ot', [
    Image.fromLocalFile('./images/off-topic.png'),
    Plain(tF.ot)
])
SimpleReply('manual', [
    Image.fromLocalFile('./images/rtfm.png'),
    Plain(tF.manual)
])
SimpleReply('ygg.server.jvm', [Plain(tF.ygg_server_jvm)])
SimpleReply('csl.gui', [Plain(tF.csl_gui)])
SimpleReply('domain', [
    Image.fromLocalFile('./images/r-search.jpg'),
    Plain(tF.domain)
])
SimpleReply('mail', [Plain(tF.mail)])
SimpleReply('csl.log', [Plain(tF.csl_log)])
SimpleReply('ygg.nsis', [Plain(tF.ygg_nsis)])
SimpleReply('browser', [
    Image.fromLocalFile('./images/browser.png'),
    Plain(tF.browser)
])
SimpleReply('ygg.client.refresh', [
    Image.fromLocalFile('./images/ygg-client-refresh.png'),
    Plain(tF.client_refresh)
])
SimpleReply('ygg.url', [
    Plain('https://littlesk.in'),
    Image.fromLocalFile('./images/ygg-url.png')
])


@bcc.receiver(GroupMessage, dispatchers=[
    *MatchKeywords(['怎么回事', '为啥', '问个问题', '请问', '问一下', '如何解决',
                    '我想问', '什么问题', '咋回事', '怎么办', '怎么解决']),
    Kanata([RegexMatch('.*为什么.*')])
])
async def new_question_nofication(app: GraiaMiraiApplication, msg: MessageChain):
    # TODO 此功能目前无法正常工作，仅能对为什么做出反应
    await app.sendGroupMessage(qq.notification_channel,
                               MessageChain.create([Plain(tF.why_notify)]),
                               quote=msg[Source][0].id)


@bcc.receiver(MemberJoinEvent)
async def memberjoinevent_listener(app: GraiaMiraiApplication, event: MemberJoinEvent):
    member = event.member
    group = member.group
    if group.id == qq.littleskin_main:
        await app.sendGroupMessage(group, MessageChain.create(
            [At(member.id), Plain(tF.join_welcome)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([MatchCommand('ygg.latest')])])
async def command_ygg_latest(app: GraiaMiraiApplication, group: Group):
    infos = await apis.AuthlibInjectorLatest.get()
    _message = f'authlib-injector 最新版本：{infos.version}\n{infos.download_url}'
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([MatchCommand('csl.latest')])])
async def command_csl_latest(app: GraiaMiraiApplication, group: Group):
    infos = await apis.CustomSkinLoaderLatest.get()
    _message = f'''CustomSkinLoader 最新版本：{infos.version}
Forge: {infos.downloads.Forge}
Fabric: {infos.downloads.Fabric}'''
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([MatchCommand('csl'), RequireParam(name='params')])])
async def command_csl(app: GraiaMiraiApplication, group: Group, params: MessageChain):
    player_name = params.asDisplay()
    result = await apis.CustomSkinLoaderApi.get('https://mcskin.littleservice.cn/csl', player_name)
    if not result.existed:
        _message = f'「{player_name}」不存在'
    else:
        _message = f'''「{player_name}」
Skin: {result.skins.slim[:7] or result.skins.default[:7]} [{result.skin_type}]
Cape: {result.cape[:7]}'''
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([MatchCommand('ygg'), RequireParam(name='params')])])
async def command_ygg(app: GraiaMiraiApplication, group: Group, params: MessageChain):
    player_name = params.asDisplay()
    littleskin_yggdrasil_root = 'https://mcskin.littleservice.cn/api/yggdrasil'
    player_uuid = await apis.YggdrasilPlayerUuidApi.get(littleskin_yggdrasil_root, player_name)
    if not player_uuid.existed:
        _message = f'「{player_name}」不存在'
    else:
        result: apis.YggdrasilGameProfileApi = await apis.YggdrasilGameProfileApi.get(littleskin_yggdrasil_root, player_uuid.id)
        textures: apis.YggdrasilTextures = result.properties.textures.textures
        _message = f'''「{result.name}」
Skin: {textures.SKIN.hash[:7] if textures.SKIN else None} [{textures.SKIN.metadata.model if textures.SKIN else None}]
Cape: {textures.CAPE.hash[:7] if textures.CAPE else None}
UUID: {UUID(player_uuid.id)}'''
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))
    

@bcc.receiver(GroupMessage, dispatchers=[Kanata([FullMatch('&ygg '), RequireParam(name='params')])])
async def command_ygg(app: GraiaMiraiApplication, group: Group, params: MessageChain):
    player_name = params.asDisplay()
    player_uuid = await api.YggdrasilPlayerUuidApi.get('https://littlesk.in/api/yggdrasil', player_name)
    if not player_uuid.existed:
        _message = f'「{player_name}」不存在'
    else:
        result = await api.YggdrasilGameProfileApi.get('https://littlesk.in/api/yggdrasil', player_uuid)
        _message = f'''「{player_name}」
皮肤：[{result.skin_type}] {result.skins.slim or result.skins.default}
披风：{result.cape}'''
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([MatchCommand('view'), RequireParam(name='params')])])
async def command_csl(app: GraiaMiraiApplication, group: Group, params: MessageChain):
    player_name = params.asDisplay()
    result = await apis.CustomSkinLoaderApi.get('https://mcskin.littleservice.cn/csl', player_name)
    if not result.existed:
        await app.sendGroupMessage(group, MessageChain.create([Plain(f'「{player_name}」不存在')]))
    else:
        skin_hash = result.skins.slim or result.skins.default
        cape_hash = result.cape
        littleskin_root = 'https://mcskin.littleservice.cn'
        preview_images: List[Image] = list()
        for texture in [skin_hash, cape_hash]:
            if skin_hash:
                preview_images.append(Image.fromUnsafeBytes(await apis.getTexturePreview(
                    littleskin_root, texture)))
    await app.sendGroupMessage(group,
                               MessageChain.create([*preview_images, Plain(f'Skin: {skin_hash[:7] if skin_hash else None} [{result.skin_type}]\nCape: {cape_hash[:7] if cape_hash else None}')]))

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


# @bcc.receiver(GroupMessage, dispatchers=[Kanata([MatchCommand('csl.config')])])
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
#     _texturehash[:7] = M.Command.args
#     if not _texturehash[:7]:
#         await app.sendGroupMessage(group, MessageChain.create([Plain(tF.view_no_hash[:7]_error)]))
#     elif len(_texturehash[:7]) != 64:
#         await app.sendGroupMessage(group, MessageChain.create([Plain(tF.view_hash[:7]_length_error)]))
#     else:
#         _image_message = PlayerProfile.getPreviewByhash[:7](_texturehash[:7])
#         if _image_message:
#             await app.sendGroupMessage(group, MessageChain.create([_image_message]))
#         else:
#             await app.sendGroupMessage(group, MessageChain.create([Plain(tF.view_not_200_error)]))


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


if __name__ == '__main__':
    app.launch_blocking()
