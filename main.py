import asyncio
from typing import List
from uuid import UUID
import aiohttp

from graia.application import GraiaMiraiApplication
from graia.application.entry import (At, Group, GroupMessage, Image,
                                     MemberJoinEvent, MessageChain, Plain,
                                     Source)
from graia.application.group import Member
from graia.application.message.elements import \
    Element as GraiaMessageElementType
from graia.application.message.elements.internal import Quote
from graia.application.message.parser.kanata import Kanata
from graia.application.message.parser.signature import RegexMatch, RequireParam
from graia.broadcast import Broadcast
from graia.broadcast.exceptions import ExecutionStop

import settings
from matchers import CommandMatch, KeywordsMatch
from models import apis
from settings import specialqq as qq
from texts import TextFields as tF

# Application & BCC 初始化
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc, connect_info=settings.Connection, enable_chat_log=False)


def SimpleReply(command: str, reply_content: List[GraiaMessageElementType]):
    async def srr_wrapper(app: GraiaMiraiApplication, group: Group):
        await app.sendGroupMessage(group, MessageChain.create(reply_content))
    bcc.receiver(GroupMessage, dispatchers=[Kanata(
        [CommandMatch(command, False)])])(srr_wrapper)


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
SimpleReply('clfcsl', [Plain(tF.clfcsl)])


@bcc.receiver(GroupMessage, dispatchers=[
    Kanata([KeywordsMatch(tF.question_keywords)])
])
async def new_question_nofication(app: GraiaMiraiApplication, group: Group, msg: MessageChain):
    enable_in_groups: List[int] = [qq.littleskin_main]
    if group.id in enable_in_groups:
        await app.sendGroupMessage(qq.notification_channel,
                                   MessageChain.create(
                                       [Plain(tF.new_question_nofication)]),
                                   quote=msg[Source][0].id)
        await app.sendGroupMessage(group,
                                   MessageChain.create(
                                       [Plain(tF.new_question_sent)]),
                                   quote=msg[Source][0].id)


@bcc.receiver(MemberJoinEvent)
async def memberjoinevent_listener(app: GraiaMiraiApplication, event: MemberJoinEvent):
    member = event.member
    group = member.group
    if group.id == qq.littleskin_main:
        await app.sendGroupMessage(group, MessageChain.create(
            [At(member.id), Plain(' '), Plain(tF.join_welcome)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([CommandMatch('ygg.latest', False)])])
async def command_handler(app: GraiaMiraiApplication, group: Group):
    infos = await apis.AuthlibInjectorLatest.get()
    _message = f'authlib-injector 最新版本：{infos.version}\n{infos.download_url}'
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([CommandMatch('csl.latest'), RequireParam(name='params')])])
async def command_handler(app: GraiaMiraiApplication, group: Group, params: MessageChain):
    infos = await apis.CustomSkinLoaderLatest.get()
    mod_loader = params.asDisplay().strip()
    forge = f'''CustomSkinLoader 最新版本：{infos.version}
Forge 1.16.5-: {infos.downloads.Forge}
Forge 1.17+: {infos.downloads.ForgeActive}'''
    fabric = f'''CustomSkinLoader 最新版本：{infos.version}
Fabric: {infos.downloads.Fabric}'''
    _message = forge if mod_loader == 'forge' else fabric
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([CommandMatch('csl'), RequireParam(name='params')])])
async def command_handler(app: GraiaMiraiApplication, group: Group, params: MessageChain):
    player_name = params.asDisplay()
    result = await apis.CustomSkinLoaderApi.get('https://mcskin.littleservice.cn/csl', player_name)
    if not result.player_existed:
        _message = f'「{player_name}」不存在'
    else:
        _message = f'''「{player_name}」
Skin: {result.skin_hash[:7]} [{result.skin_type}]
Cape: {result.cape_hash[:7] if result.cape_existed else None}'''
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([CommandMatch('ygg'), RequireParam(name='params')])])
async def command_handler(app: GraiaMiraiApplication, group: Group, params: MessageChain):
    player_name = params.asDisplay()
    littleskin_yggdrasil_root = 'https://mcskin.littleservice.cn/api/yggdrasil'
    player_uuid = await apis.YggdrasilPlayerUuidApi.get(littleskin_yggdrasil_root, player_name)
    if not player_uuid.existed:
        _message = f'「{player_name}」不存在'
    else:
        result: apis.YggdrasilGameProfileApi = await apis.YggdrasilGameProfileApi.get(littleskin_yggdrasil_root, player_uuid.id)
        textures: apis.YggdrasilTextures = result.properties.textures.textures
        _message = f'''「{result.name}」
Skin: {textures.SKIN.hash[:7] if textures.SKIN else None} [
    {textures.SKIN.metadata.model if textures.SKIN else None}]
Cape: {textures.CAPE.hash[:7] if textures.CAPE else None}
UUID: {UUID(player_uuid.id)}'''
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([CommandMatch('view'), RequireParam(name='params')])])
async def command_handler(app: GraiaMiraiApplication, group: Group, params: MessageChain):
    player_name = params.asDisplay()
    result = await apis.CustomSkinLoaderApi.get('https://mcskin.littleservice.cn/csl', player_name)
    if not result.player_existed:
        await app.sendGroupMessage(group, MessageChain.create([Plain(f'「{player_name}」不存在')]))
    else:
        bs_root = 'https://mcskin.littleservice.cn'
        preview_images: List[Image] = list()
        for texture in [result.skin_hash, result.cape_hash]:
            if texture:
                preview_images.append(Image.fromUnsafeBytes(await apis.getTexturePreview(
                    bs_root, texture)))
    await app.sendGroupMessage(group,
                               MessageChain.create([*preview_images,
                                                    Plain(f'''「{player_name}」
Skin: {result.skin_hash[:7]} [{result.skin_type}]
Cape: {result.cape_hash[:7] if result.cape_existed else None}''')]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([CommandMatch('view.mojang'), RequireParam(name='params')])])
async def command_handler(app: GraiaMiraiApplication, group: Group, params: MessageChain):
    player_name = params.asDisplay()
    player_uuid = await apis.MojangPlayerUuidApi.get(player_name)
    if not player_uuid.existed:
        await app.sendGroupMessage(group, MessageChain.create([Plain(f'「{player_name}」不存在')]))
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://crafatar.com/renders/body/{player_uuid.id}?overlay') as resp:
            if resp.status == 200:
                image = await resp.content.read()
                await app.sendGroupMessage(group, MessageChain.create([Image.fromUnsafeBytes(image)]))
            else:
                err_msg = await resp.text()
                await app.sendGroupMessage(group, MessageChain.create([Plain(f'Crafatar Error: {err_msg.strip()[:64]}')]))


@bcc.receiver("GroupMessage", dispatchers=[Kanata([RegexMatch(r'^草*$')])])
async def grass_spammer(app: GraiaMiraiApplication, group: Group, msg: MessageChain):
    disable_in_groups: List[int] = [qq.littleskin_main, qq.csl_group]
    if not group.id in disable_in_groups:
        await app.sendGroupMessage(group,
                                   MessageChain.create(
                                       [Plain('\u202e草')]))


@bcc.receiver(GroupMessage, dispatchers=[Kanata([CommandMatch('revoke', False)])])
async def command_handler(app: GraiaMiraiApplication, messagechain: MessageChain):
    if Quote in messagechain:
        origin_message = messagechain[Quote][0].origin[Source][0]
        current_message = messagechain[Source][0]
        await app.revokeMessage(origin_message)
        await app.revokeMessage(current_message)


@bcc.receiver(GroupMessage, dispatchers=[Kanata([CommandMatch('mute ', False)])])
async def command_handler(app: GraiaMiraiApplication, group: Group, member: Member, messagechain: MessageChain):
    admins = await app.memberList(qq.notification_channel)
    admins_id = [m.id for m in admins]
    if member.id in admins_id and At in messagechain:
        target_members: List[At] = messagechain[At]
        targets = [m.target for m in target_members]
        for target in targets:
            await app.mute(group, target, 60 * 10)


@bcc.receiver(GroupMessage, dispatchers=[Kanata([CommandMatch('unmute ', False)])])
async def command_handler(app: GraiaMiraiApplication, group: Group, member: Member, messagechain: MessageChain):
    admins = await app.memberList(qq.notification_channel)
    admins_id = [m.id for m in admins]
    if member.id in admins_id and At in messagechain:
        target_members: List[At] = messagechain[At]
        targets = [m.target for m in target_members]
        for target in targets:
            await app.unmute(group, target)


@bcc.receiver(GroupMessage)
async def wrong_usage_tips(app: GraiaMiraiApplication, group: Group, messagechain: MessageChain):
    msg_text = messagechain.asDisplay()
    if msg_text.startswith(('&mute ', '&unmute')) and msg_text.endswith(' '):
        await app.sendGroupMessage(group, MessageChain.create([Plain('请删除末尾空格后重试')]))


if __name__ == '__main__':
    app.launch_blocking()
