from uuid import UUID

from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Group
from graia.saya import Channel

from models.apis import (CustomSkinLoaderApi, YggdrasilGameProfileApi,
                         YggdrasilPlayerUuidApi, YggdrasilTextures)

channel = Channel.current()

@channel.use(CommandSchema('&csl {player_name: str}'))
async def csl(app: Ariadne, group: Group, player_name: str):
    result = await CustomSkinLoaderApi.get('https://littleskin.cn/csl', player_name)
    if not result.player_existed:
        _message = f'「{player_name}」不存在'
    else:
        _message = f'''「{player_name}」
Skin: {result.skin_hash[:8] if result.skin_existed else None} [{result.skin_type if result.skin_existed else None}]
Cape: {result.cape_hash[:8] if result.cape_existed else None}'''
    await app.send_message(group, MessageChain([Plain(_message)]))

@channel.use(CommandSchema('&ygg {player_name: str}'))
async def ygg(app: Ariadne, group: Group, player_name: str):
    littleskin_yggdrasil_root = 'https://littleskin.cn/api/yggdrasil'
    player_uuid = await YggdrasilPlayerUuidApi.getBlessingSkinServer(littleskin_yggdrasil_root, player_name)
    if not player_uuid.existed:
        _message = f'「{player_name}」不存在'
    else:
        result: YggdrasilGameProfileApi = await YggdrasilGameProfileApi.getBlessingSkinServer(littleskin_yggdrasil_root, player_uuid.id)
        textures: YggdrasilTextures = result.properties.textures.textures
        _message = f'''「{result.name}」
Skin: {textures.SKIN.hash[:8] if textures.SKIN else None} [{textures.SKIN.metadata.model if textures.SKIN else None}]
Cape: {textures.CAPE.hash[:8] if textures.CAPE else None}
UUID: {UUID(player_uuid.id)}'''
    await app.send_message(group, MessageChain([Plain(_message)]))
