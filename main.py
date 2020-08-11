import asyncio

import requests

import botmessages
import botpermissions
import player
import settings
from mirai import (At, Group, GroupMessage, Image, MemberJoinEvent,
                   MessageChain, Mirai, Plain, Quote)

app = Mirai(settings.mirai_url)


@app.receiver("MemberJoinEvent")
async def member_join(app: Mirai, event: MemberJoinEvent):
    group_id = event.member.group.id
    if group_id == 586146922:  # [user@LittleSkin ~/group/QQ]$
        await app.sendGroupMessage(  # 刷新群名片
            event.member.group.id, [
                Plain(text="!!name")
            ])
        await app.sendGroupMessage(
            event.member.group.id, [
                At(target=event.member.id),
                Plain(text="欢迎！要使用清晰的语言描述你的情况哦~")
            ])
    elif group_id == 651672723:  # Honoka Café
        await app.sendGroupMessage(  # 刷新群名片
            event.member.group.id, [
                Plain(text="!!name")
            ])


@app.receiver("GroupMessage")
async def event_gm(app: Mirai, group: Group, message: MessageChain, event: GroupMessage):
    # 一些常量
    message_plain = botmessages.getAll(message.getAllofComponent(Plain))
    message_at = message.getFirstComponent(At)
    messageId = message.getSource().id
    senderId = event.sender.id

    Operator = botpermissions.groupPermissions(senderId)

    if message_plain and not Operator.isBlocked():  # 如果有纯文本且没有被封禁
        if senderId == 3426549342 and '：' in message_plain:  # Constance 消息同步机器人
            message_plain = message_plain.split('：', 1)[1]  # overwrite

        _spilted_message = message_plain.split(' ', 1)

        # 指令常量
        command = _spilted_message[0]
        args = _spilted_message[1] if len(_spilted_message) > 1 else None

        # Commands
        if command == '$csl':  # csl
            if args:  # 参数方式
                _player_name = args
            else:  # 回复方式
                _player_name = botmessages.getQuote(
                    message.getFirstComponent(Quote).origin)

            thisPlayer = player.PlayerProfile(_player_name)
            send_message = thisPlayer.getCsl()
            await app.sendGroupMessage(group, send_message)
        elif command == '$csl.log':
            await app.sendGroupMessage(group, [
                Plain(
                    text='CustomSkinLoader 的日志位于 .minecraft/CustomSkinLoader/CustomSkinLoader.log，请将此文件直接上传至群文件')
            ])
        elif command == '$csl.json':
            await app.sendGroupMessage(group, [
                Plain(
                    text='请参照「手动修改配置文件」\nhttps://manual.littlesk.in/newbee/mod.html#%E6%89%8B%E5%8A%A8%E4%BF%AE%E6%94%B9%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6')
            ])
        elif command == '$ygg':
            if args:
                _player_name = args
            else:
                _player_name = botmessages.getQuote(
                    message.getFirstComponent(Quote).origin)

            thisPlayer = player.PlayerProfile(_player_name)
            send_message = thisPlayer.getYgg()
            await app.sendGroupMessage(group, send_message)
        elif command == '$ygg.nsis':
            await app.sendGroupMessage(group, [
                Image.fromFileSystem("./images/rtfm.png"),
                Plain(text='请确认服务器正确配置 authlib-injector 并将 online-mode 设为 true，否则请使用 CustomSkinLoader。\n更多：https://manual.littlesk.in/advanced/yggdrasil.html')]
            )
        elif command == '$texture':
            _texture_hash = args
            if len(_texture_hash) != 64:
                await app.sendGroupMessage(group, [Plain(text='[ERROR] Hash 长度有误')])
            else:
                _image_message = player.PlayerProfile.getPreviewByHash(_texture_hash)
                if _image_message:
                    await app.sendGroupMessage(group, [_image_message])
                else:
                    await app.sendGroupMessage(group, [Plain(text='[ERROR]')])
        elif command == '$browser':
            await app.sendGroupMessage(group, [
                Image.fromFileSystem("./images/browser.png"),
                Plain(
                    text='Chrome: https://www.google.cn/chrome\nFirefox: https://www.mozilla.org/zh-CN/firefox/new/')
            ])
        elif command == '$mail':
            await app.sendGroupMessage(group, [Plain(text='请发送邮件至 support@littlesk.in，并在邮件中详细说明你的情况\n更多：https://manual.littlesk.in/email.html')])
        elif command == '$faq':
            await app.sendGroupMessage(group, [
                Image.fromFileSystem("./images/rtfm.png"),
                Plain(text='你需要去阅读一遍 常见问题解答。\nhttps://manual.littlesk.in/faq.html')]
        elif command == '$ot':
            await app.sendGroupMessage(group, [
                Image.fromFileSystem("./images/off-topic.png"),
                Plain(text='闲聊请前往 Honoka Café，群号 651672723')]
        elif command == '$url':
            await app.sendGroupMessage(group, [Plain(text='你可能仍在使用 littleskin.cn ，该域名已在国内下线。\n我们强烈建议你去使用 littlesk.in 来获取最佳体验。')])
            )
        elif command == '$ban':
            if message_at:  # at
                userqq = message_at.target
                displayname = message_at.display
            else:  # QQ 号
                userqq = int(args)
                displayname = int(args)
            _User = botpermissions.groupPermissions(userqq)
            if Operator.isAdmin() and not _User.isAdmin():
                _status = Operator.block(userqq)
                if _status:
                    send_message = f'{displayname} 已被管理员封禁。'
                else:
                    send_message = f'{displayname} 已经在封禁列表中。'
                await app.sendGroupMessage(group, [
                    Plain(
                        text=send_message)
                ])
        elif command == '$unban':
            if message_at:  # at
                userqq = message_at.target
                displayname = message_at.display
            else:  # QQ 号
                userqq = int(args)
                displayname = int(args)

            _User = botpermissions.groupPermissions(userqq)
            if Operator.isAdmin():
                _status = Operator.unblock(userqq)
                if _status:
                    send_message = f'{displayname} 已被管理员解封。'
                else:
                    send_message = f'{displayname} 并不在封禁列表中。'
                await app.sendGroupMessage(group, [
                    Plain(
                        text=send_message)
                ])
        elif command == '$help':
            await app.sendGroupMessage(group, [
                Plain(
                    text='请查看 https://littleskin-commspt-bot-manual.netlify.app/')
            ])

if __name__ == "__main__":
    app.run()
