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


@channel.use(CommandSchema('&csl.latest {mod_loader: str = "fabric"}'))
async def csl_latest(app: Ariadne, group: Group, mod_loader: str):
    infos = await CustomSkinLoaderLatest.get()
    forge = f'''CustomSkinLoader (Forge) 最新版本：{infos.version}
1.7.10 ~ 1.16.5: {infos.downloads.Forge}
1.17+: {infos.downloads.ForgeActive}'''
    fabric = f'''CustomSkinLoader (Fabric) 最新版本：{infos.version}
Fabric: {infos.downloads.Fabric}'''
    _messages = {'fabric': fabric, 'forge': forge}
    await app.sendGroupMessage(group, MessageChain([Plain(_messages[mod_loader])]))


@channel.use(CommandSchema('&java.latest {type: str = "jre"} {version: int = "8"}'))
async def java_latest(app: Ariadne, group: Group, version: int, type: str):
    url = getLiberica(version, type)
    await app.sendGroupMessage(group, MessageChain([Plain(f'''
最新 Liberica {type}{version} 下载地址：
{url}
    ''')]))
