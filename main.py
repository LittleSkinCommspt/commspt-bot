import asyncio
from typing import List, Optional

import requests
from graia.application import GraiaMiraiApplication
from graia.application.entry import (At, Group, GroupMessage, Image,
                                     MemberCardChangeEvent, MemberJoinEvent,
                                     MessageChain, Plain)
from graia.broadcast import Broadcast
from graia.broadcast.builtin.decoraters import Depend

import settings
from botpermissions import groupPermissions
from commandparser import (CommandParser,
                           onCommand, onWord, onWords, onMatch, exceptGroups, filterCafe, adminOnly)
from csllogparser import aoscPastebin
from player import PlayerProfile
from texts import TextFields as tF
from githublistener import githubListener

# Application & BCC 初始化
loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(broadcast=bcc, connect_info=settings.Connection)

# GitHub Listener
async def _send(message: str):
    await app.sendGroupMessage(settings.specialqq.commspt_group, MessageChain.create([Plain(message)]))

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
    if group.id in [
        settings.specialqq.littleskin_main,
        settings.specialqq.littleskin_cafe,
        settings.specialqq.csl_group
    ]:
        await app.sendGroupMessage(group, MessageChain.create(
            [Plain(tF.constance_refresh_name)]))


# 指令监听
@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('help'))])
async def command_help(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.help)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('manual'))])
async def command_manual(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile('./images/rtfm.png'),
        Plain(tF.manual)
    ]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('faq'))])
async def command_faq(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile('./images/rtfm.png'),
        Plain(tF.faq)
    ]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ygg.server.jvm'))])
async def command_ygg_server_jvm(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.ygg_server_jvm)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('domain'))])
async def command_domain(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.domain)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('mail')),
                                                 Depend(exceptGroups([settings.specialqq.csl_group]))])
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


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('clfcsl.latest'))])
async def command_csl_latest(app: GraiaMiraiApplication, group: Group):
    _r = requests.get(
        'https://csl-1258131272.cos.ap-shanghai.myqcloud.com/latest.json')
    _j: dict = _r.json()
    _latestVersion = _j['version']
    _forge = _j['downloads']['Forge']
    _message = f'''CustomSkinLoader 最新版本：{_latestVersion}
Forge: {_forge}
{tF.clfcsl_latest}'''
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('csl.config'))])
async def command_csl_config_littleskin(app: GraiaMiraiApplication, group: Group):
    _message: str = tF.csl_config_csl_group if group.id == settings.specialqq.csl_group else tF.csl_config_littleskin
    await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('csl.log'))])
async def command_csl_log(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.csl_log)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ygg.nsis'))])
async def command_ygg_nsis(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.ygg_nsis)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('browser'))])
async def command_browser(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile('./images/browser.png'),
        Plain(tF.browser)
    ]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ygg.client.refresh'))])
async def command_ygg_client_refresh(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile('./images/ygg-client-refresh.png'),
        Plain(tF.client_refresh)
    ]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ot')), Depend(filterCafe)])
async def command_ot(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    CP = CommandParser(_gm, settings.commandSymbol)
    atList: List[Optional[At]] = [At(t.target)
                                  for t in CP.at] if CP.at != [] else []
    await app.sendGroupMessage(group, MessageChain.create([
        *atList,
        Image.fromLocalFile('./images/off-topic.png'),
        # 仅在 LittleSkin 主群中启用此文本消息
        *([Plain(tF.ot)] if group.id == settings.specialqq.littleskin_main else [])
    ]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('view'))])
async def command_view(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    CP = CommandParser(_gm, settings.commandSymbol)
    _textureHash = CP.Command.args
    if not _textureHash:
        await app.sendGroupMessage(group, MessageChain.create([Plain(tF.view_no_hash_error)]))
    elif len(_textureHash) != 64:
        await app.sendGroupMessage(group, MessageChain.create([Plain(tF.view_hash_length_error)]))
    else:
        _image_message = PlayerProfile.getPreviewByHash(_textureHash)
        if _image_message:
            await app.sendGroupMessage(group, MessageChain.create([_image_message]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain(tF.view_not_200_error)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('csl'))])
async def command_csl(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    CP = CommandParser(_gm, settings.commandSymbol)
    _playerName = CP.Command.args if CP.Command.args else CP.quote_plain_message
    _player = PlayerProfile(_playerName)
    _message = _player.getCsl()
    await app.sendGroupMessage(group, MessageChain.create(_message))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ygg'))])
async def command_ygg(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    CP = CommandParser(_gm, settings.commandSymbol)
    _playerName = CP.Command.args if CP.Command.args else CP.quote_plain_message
    _player = PlayerProfile(_playerName)
    _message = _player.getYgg()
    await app.sendGroupMessage(group, MessageChain.create(_message))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ban')), Depend(adminOnly)])
async def command_ban(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    CP = CommandParser(_gm, settings.commandSymbol)

    def add() -> str:
        _l = str()
        for t in CP.at:
            targetGP = groupPermissions(t.target)
            if not targetGP.isAdmin():
                _result = targetGP.blockme()
                _message = f'{t.display} {tF.ban.add_succ}\n' if _result else f'{t.display} {tF.ban.add_fail}\n'
                _l = f'{_l}{_message}'
        return _l.strip('\n')

    def remove() -> str:
        _l = str()
        for t in CP.at:
            targetGP = groupPermissions(t.target)
            _result = targetGP.unblockme()
            _message = f'{t.display} {tF.ban.remove_succ}\n' if _result else f'{t.display} {tF.ban.remove_fail}\n'
            _l = f'{_l}{_message}'
        return _l.strip('\n')

    if CP.Command.args:
        subCommand = CP.Command.argsList[0]
        if subCommand == 'add':
            await app.sendGroupMessage(group, MessageChain.create([Plain(add())]))
        if subCommand == 'remove':
            await app.sendGroupMessage(group, MessageChain.create([Plain(remove())]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onWord('https://pastebin.aosc.io/paste/'))])
async def parse_csl_log(app: GraiaMiraiApplication, group: Group, _gm: GroupMessage):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.csl_log_parsing)]))
    CP = CommandParser(_gm, settings.commandSymbol)
    fromLs = group.id in [
        settings.specialqq.littleskin_main,
        settings.specialqq.littleskin_cafe
    ]
    try:
        _message = aoscPastebin(CP.plain_message, fromLittleSkin=fromLs)
        await app.sendGroupMessage(group, MessageChain.create([Plain(_message)]))
    except Exception as e:
        await app.sendGroupMessage(group, MessageChain.create([Plain(repr(e))]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('test'))])
async def command_test(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain(tF.test)]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onWords(['网易lj', '迷你lj', '翻墙', 'vpn']))])
async def anti_bad_words(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain('请不要在此群中讨论有关话题！')]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onMatch(r'^草*$')),
                                                 Depend(exceptGroups([settings.specialqq.littleskin_main]))])
async def grass_spammer(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([Plain('草\u202e')]))


@bcc.receiver(GroupMessage, headless_decoraters=[Depend(onCommand('ygg.url'))])
async def command_ygg_url(app: GraiaMiraiApplication, group: Group):
    await app.sendGroupMessage(group, MessageChain.create([
        Image.fromLocalFile('./images/ygg-url.png')
    ]))


if __name__ == '__main__':
    app.subscribe_atexit()
    graia_task = app.create_background_task()
    github_tasks = githubListener(_send)
    future = asyncio.wait([graia_task, *github_tasks])
    loop.run_until_complete(future)
