from mirai import Mirai, Plain, At, Image, Quote, MessageChain, Group, GroupMessage, MemberJoinEvent
import asyncio

import botmessages
import csl
import permission

import settings

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


@app.receiver("GroupMessage")
async def event_gm(app: Mirai, group: Group, message: MessageChain, event: GroupMessage):
    # 一些常量
    message_plain = botmessages.getAll(message.getAllofComponent(Plain))
    message_at = message.getFirstComponent(At)
    messageId = message.getSource().id
    senderId = event.sender.id

    if message_plain and not permission.isblocked(senderId):  # 如果有纯文本且没有被封禁
        _spilted_message = message_plain.split(' ', 1)
        
        # 另一些常量
        command = _spilted_message[0]
        args = _spilted_message[1] if len(_spilted_message) > 1 else None

        # Commands
        if command == '$csl':  # csl
            if args:  # 参数方式
                send_message = csl.getPlayerInfo(args)
            else:  # 回复方式
                _player_name = botmessages.getQuote(
                    message.getFirstComponent(Quote).origin)
                send_message = csl.getPlayerInfo(_player_name)
            await app.sendGroupMessage(group, [
                send_message  # 返回一个 Plain 对象
            ])
        elif command == '$csl.log':
            send_message = csl.showLog()
            await app.sendGroupMessage(group, [
                send_message  # 返回一个 Plain 对象
            ])
        elif command == '$browser':
            await app.sendGroupMessage(group, [
                Image.fromFileSystem("./images/browser.png"),
                Plain(
                    text='Chrome: https://www.google.cn/chrome\nFirefox: https://www.mozilla.org/zh-CN/firefox/new/')
            ])
        elif command == '$mail':
            await app.sendGroupMessage(group, [
                Plain(
                    text='请发送邮件至 support@littlesk.in，并在邮件中详细说明你的情况\n更多：https://manual.littlesk.in/email.html')
            ])
        elif command == '$faq':
            await app.sendGroupMessage(group, [
                Plain(
                    text='你应该阅读一遍 常见问题解答\nhttps://manual.littlesk.in/faq.html')
            ])
        elif command == '$ot':
            await app.sendGroupMessage(group, [
                Image.fromFileSystem("./images/off-topic.png"),
                Plain(
                    text='闲聊请前往 Honoka Café，群号 651672723')
            ])
        elif command == '$ban':
            if message_at:  # at
                userqq = message_at.target
                displayname = message_at.display
            else:  # QQ 号
                userqq = int(args)
                displayname = int(args)
            if permission.check(senderId) and not permission.check(userqq):
                _status = permission.blockuser(userqq)
                if _status:
                    send_message = f'已封禁 {displayname}，请不要滥用机器人！'
                else:
                    send_message = f'{displayname} 已经在封禁列表中'
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
            if permission.check(senderId):
                _status = permission.allowuser(userqq)
                if _status:
                    send_message = f'已解封 {displayname}'
                else:
                    send_message = f'{displayname} 并不在封禁列表中'
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
