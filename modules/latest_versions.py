from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.ariadne.message.commander.saya import CommandSchema
from models.apis import AuthlibInjectorLatest, CustomSkinLoaderLatest, getLiberica

channel = Channel.current()

@channel.use(CommandSchema('&ygg.latest'))
async def ygg_latest(app: Ariadne, group: Group):
    infos = await AuthlibInjectorLatest.get()
    _message = f'authlib-injector 最新版本：{infos.version}\n{infos.download_url}'
    await app.send_message(group, MessageChain([Plain(_message)]))


@channel.use(CommandSchema('&java.latest {version: int = "8"} {type: str = "jre"}'))
async def java_latest(app: Ariadne, group: Group, version: int, type: str):
    url = await getLiberica(version, type)
    await app.sendGroupMessage(group, MessageChain([Plain(f'''
最新 Liberica {type}{version} 下载地址：
{url}
    ''')]))
