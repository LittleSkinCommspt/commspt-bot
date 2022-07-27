from typing import List

from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.element import Element, Image, Plain
from graia.ariadne.model import Group
from graia.saya import Channel
from texts import TextFields as tF
from settings import specialqq as qq


channel = Channel.current()


def SimpleReply(command: str, reply_content: List[Element]):
    async def srr_wrapper(app: Ariadne, group: Group):
        await app.send_message(group, MessageChain(reply_content))
    channel.use(CommandSchema(f'&{command}'))(srr_wrapper)



SimpleReply('ping', [Plain('Pong!')])

SimpleReply('help', [Plain(tF.help)])
SimpleReply('log.minecraft', [Plain(tF.log_minecraft)])
SimpleReply('log.launcher', [Plain(tF.log_launcher)])
SimpleReply('java8.latest', [Plain(tF.java8_latest)])
SimpleReply('java.latest', [Plain(tF.java_latest)])
SimpleReply('hmcl.latest', [Plain(tF.hmcl_latest)])
SimpleReply('manual', [
    Image(path='./images/rtfm.png'),
    Plain(tF.manual)
])
SimpleReply('mail', [Plain(tF.mail)])
SimpleReply('browser', [
    Image(path='./images/browser.png'),
    Plain(tF.browser)
])
SimpleReply('ygg.url', [
    Plain('https://littlesk.in'),
    Image(path='./images/ygg-url.png')
])
SimpleReply('ygg.nsis', [Plain(tF.ygg_nsis)])
SimpleReply('ygg.server.jvm', [Plain(tF.ygg_server_jvm)])
SimpleReply('ygg.client.refresh', [
    Image(path='./images/ygg-client-refresh.png'),
    Plain(tF.client_refresh)
])
SimpleReply('csl.log', [Plain(tF.csl_log)])
SimpleReply('csl.gui', [Plain(tF.csl_gui)])
SimpleReply('clfcsl', [Plain(tF.clfcsl)])
