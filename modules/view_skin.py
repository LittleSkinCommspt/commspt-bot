from typing import List

import aiohttp
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.element import Image, Plain
from graia.ariadne.model import Group
from graia.saya import Channel
from models.apis import (CustomSkinLoaderApi, MojangPlayerUuidApi,
                         getTexturePreview)

channel = Channel.current()


@channel.use(CommandSchema('&view {player_name: str}'))
async def view(app: Ariadne, group: Group, player_name: str):
    result = await CustomSkinLoaderApi.get('https://littleskin.cn/csl', player_name)
    if not result.player_existed:
        await app.send_message(group, MessageChain([Plain(f'「{player_name}」不存在')]))
    else:
        bs_root = 'https://littleskin.cn'
        preview_images: List[Image] = list()
        for texture in [result.skin_hash, result.cape_hash]:
            if texture:
                preview_images.append(Image(data_bytes=await getTexturePreview(
                    bs_root, texture)))
                await app.send_message(group,
                                       MessageChain([*preview_images,
                                                     Plain(f'''「{player_name}」
Skin: {result.skin_hash[:8]} [{result.skin_type}]
Cape: {result.cape_hash[:8] if result.cape_existed else None}''')]))


@channel.use(CommandSchema('&view.mojang {player_name: str}'))
async def view(app: Ariadne, group: Group, player_name: str):
    player_uuid = await MojangPlayerUuidApi.get(player_name)
    if not player_uuid.existed:
        await app.send_message(group, MessageChain([Plain(f'「{player_name}」不存在')]))
        return
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://crafatar.com/renders/body/{player_uuid.id}?overlay') as resp:
            if resp.status == 200:
                image = await resp.content.read()
                await app.send_message(group, MessageChain([Image(data_bytes=image)]))
            else:
                err_msg = await resp.text()
                await app.send_message(group, MessageChain([Plain(f'Crafatar Error: {err_msg.strip()[:64]}')]))
