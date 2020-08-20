import asyncio

import requests
from graia.application import GraiaMiraiApplication
from graia.application.entry import (At, Group, GroupMessage, Image,
                                     MemberCardChangeEvent, MemberJoinEvent,
                                     MessageChain, Plain)
from graia.broadcast import Broadcast
from graia.broadcast.builtin.decoraters import Depend

import settings
from botpermissions import groupPermissions
from commandparser import CommandParser, onCommand, filterCafe
from player import PlayerProfile
from texts import TextFields as tF

# Application & BCC 初始化
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(broadcast=bcc, connect_info=settings.Connection)


# 刷新群名片
@bcc.receiver(MemberJoinEvent)
async def memberjoinevent_listener(app: GraiaMiraiApplication, event: MemberJoinEvent):
    member = event.member
    group = member.group
    if group.id == settings.specialqq.littleskin_main:
        await app.sendGroupMessage(group, MessageChain.create(
            [Plain(tF.constance_refresh_name)]))
        await app.sendGroupMessage(group, MessageChain.create(
            [At(member.id), Plain(tF.welcome_to_littleskin)]))
    elif group.id == settings.specialqq.littleskin_cafe:
        await app.sendGroupMessage(group, MessageChain.create(
            [Plain(tF.constance_refresh_name)]))


@bcc.receiver(MemberCardChangeEvent)
async def membercardchangeevent_listener(app: GraiaMiraiApplication, event: MemberCardChangeEvent):
    member = event.member
    group = member.group
    GP = groupPermissions(member.id)  # 防止滥用
    if GP.isBlocked():
        return None
    if group.id in [settings.specialqq.littleskin_main, settings.specialqq.littleskin_cafe]:
        await app.sendGroupMessage(group, MessageChain.create(
            [Plain(tF.constance_refresh_name)]))


# 指令监听
@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('help'))])
async def command_help(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.help)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('manual'))])
async def command_manual(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.manual)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ygg.server.jvm'))])
async def command_ygg_server_jvm(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.ygg_server_jvm)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('domain'))])
async def command_domain(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.domain)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('mail'))])
async def command_mail(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.mail)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ygg.latest'))])
async def command_ygg_latest(app: GraiaMiraiApplication, group: Group):
    _r = requests.get(
        'https://authlib-injector.yushi.moe/artifact/latest.json')
    _j: dict = _r.json()
    _latestVersion = _j['version']
    _url = _j['download_url']
    _message = f'authlib-injector 最新版本：{_latestVersion}\n{_url}'
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('csl.latest'))])
async def command_csl_latest(app: GraiaMiraiApplication, group: Group):
    _r = requests.get(
        'https://csl-1258131272.cos.ap-shanghai.myqcloud.com/latest.json')
    _j: dict = _r.json()
    _latestVersion = _j['version']
    _forge = _j['downloads']['Forge']
    _fabric = _j['downloads']['Fabric']
    _message = f'''CustomSkinLoader 最新版本：{_latestVersion}
Forge: {_forge}
Fabric: {_fabric}'''
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('csl.json'))])
async def command_csl_json(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.csl_json)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ygg.nsis'))])
async def command_ygg_nsis(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.ygg_nsis)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('browser'))])
async def command_browser(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile('./images/browser.png'),
        Plain(tF.browser)
    ]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ot')), Depend(filterCafe)])
async def command_ot(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile('./images/off-topic.png'),
        Plain(tF.ot)
    ]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('view'))])
async def command_csl(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    CP = CommandParser(_gm, settings.commandSymbol)
    _textureHash = CP.Command.args
    if len(_textureHash) != 64:
        await app.sendGroupMessage(group, MessageChain.create(tF.view_hash_length_error))
    else:
        _image_message = PlayerProfile.getPreviewByHash(_textureHash)
        if _image_message:
            await app.sendGroupMessage(group, MessageChain.create(_image_message))
        else:
            await app.sendGroupMessage(group, MessageChain.create(tF.view_not_200_error))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('csl'))])
async def command_csl(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    CP = CommandParser(_gm, settings.commandSymbol)
    _playerName = CP.Command.args if CP.Command.args else CP.quote_plain_message
    _player = PlayerProfile(_playerName)
    _message = _player.getCsl()
    await app.sendGroupMessage(group, MessageChain.create(_message))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ygg'))])
async def command_csl(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    CP = CommandParser(_gm, settings.commandSymbol)
    _playerName = CP.Command.args if CP.Command.args else CP.quote_plain_message
    _player = PlayerProfile(_playerName)
    _message = _player.getYgg()
    await app.sendGroupMessage(group, MessageChain.create(_message))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ban'))])
async def command_test(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    CP = CommandParser(_gm, settings.commandSymbol)
    GP = groupPermissions(CP.sender_id)
    if GP.isAdmin():
        for t in CP.at:
            targetGP = groupPermissions(t.target)
            if not targetGP.isAdmin():
                _result = targetGP.blockme()
                _message = f'{t.display} 因滥用而被封禁' if _result else f'失败，{t.display} 已在封禁列表中'
                await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('unban'))])
async def command_test(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    CP = CommandParser(_gm, settings.commandSymbol)
    GP = groupPermissions(CP.sender_id)
    if GP.isAdmin():
        for t in CP.at:
            targetGP = groupPermissions(t.target)
            _result = targetGP.unblockme()
            _message = f'{t.display} 解除封禁成功' if _result else f'失败，{t.display} 不在封禁列表中'
            await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('test'))])
async def command_test(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.test)]))


if __name__ == '__main__':
    app.launch_blocking()
