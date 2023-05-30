from typing import List, Optional

import aiohttp
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.element import Image, Plain
from graia.ariadne.model import Group
from graia.saya import Channel
from models.apis import (
    CustomSkinLoaderApi,
    LegacyApi,
    getTexturePreview,
)

channel = Channel.current()


async def request_skinrendermc(
    skin_url: Optional[str], cape_url: Optional[str], name_tag: Optional[str]
):
    p = {
        "skinUrl": skin_url,
        "capeUrl": cape_url,
        "nameTag": name_tag,
    }

    # 删除值为 None 的键值对
    # （SkinRenderMC 只判断键值对是否存在）
    for x in [k for k in p if not p[k]]:
        p.pop(x)

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://10.50.0.4:57680/url/image/both",
            params=p,
            timeout=30,  # 通常只需要不到 15 秒
        ) as resp:
            if resp.status == 200:
                image = await resp.content.read()
                return Image(data_bytes=image)
            else:
                return


@channel.use(CommandSchema("&view.csl {player_name: str}"))
async def customskinloader(app: Ariadne, group: Group, player_name: str):
    result = await CustomSkinLoaderApi.get("https://littleskin.cn/csl", player_name)
    if not result.player_existed:
        await app.send_message(group, MessageChain([Plain(f"「{player_name}」不存在")]))
    else:
        bs_root = "https://littleskin.cn"
        preview_images: List[Image] = list()
        for texture_hash in [result.skin_hash, result.cape_hash]:
            if texture_hash:
                preview_images.append(
                    Image(data_bytes=await getTexturePreview(bs_root, texture_hash))
                )
        await app.send_message(
            group,
            MessageChain(
                [
                    *preview_images,  # 解构，有几个图就显示几个图
                    # hash 只截取前 8 位
                    # TODO 以后会做函数来进行截取
                    Plain(
                        f"""「{player_name}」
Skin: {result.skin_hash[:8]} [{result.skin_type}]
Cape: {result.cape_hash[:8] if result.cape_existed else None}

via SkinRenderMC, CustomSkinLoader API"""
                    ),
                ]
            ),
        )


@channel.use(CommandSchema("&view.ygg {player_name: str}"))
async def yggdrasil(app: Ariadne, group: Group, player_name: str):
    # TODO
    await app.send_message(group, MessageChain([Plain(f"此功能等待重构")]))
    return

    api_root = "https://littleskin.cn/api/yggdrasil"

    player_uuid = await YggdrasilPlayerUuidApi.getBlessingSkinServer(
        api_root, player_name
    )
    if not player_uuid.existed:
        await app.send_message(group, MessageChain([Plain(f"「{player_name}」不存在")]))
        return

    await app.send_message(group, MessageChain([Plain("[SkinRenderMC] 需要一些时间来处理你的请求")]))

    player_profile = await YggdrasilGameProfileApi.getBlessingSkinServer(
        api_root, player_uuid.id
    )

    generated_image = await request_skinrendermc(
        player_profile.properties.textures.textures.SKIN.url,
        player_profile.properties.textures.textures.CAPE.url,
        player_uuid.name,
    )

    if generated_image:
        await app.send_message(
            group,
            MessageChain(
                [
                    generated_image,
                    Plain("\nvia SkinRenderMC, Yggdrasil API"),
                ]
            ),
        )
    else:
        await app.send_message(
            group,
            MessageChain([Plain("SkinRenderMC API Error")]),
        )


@channel.use(CommandSchema("&view.mojang {player_name: str}"))
async def mojang(app: Ariadne, group: Group, player_name: str):
    # TODO
    await app.send_message(group, MessageChain([Plain(f"此功能等待重构")]))
    return

    player_uuid = await YggdrasilPlayerUuidApi.getMojangServer(player_name)
    if not player_uuid.existed:
        await app.send_message(group, MessageChain([Plain(f"「{player_name}」不存在")]))
        return

    await app.send_message(group, MessageChain([Plain("[SkinRenderMC] 需要一些时间来处理你的请求")]))

    player_profile = await YggdrasilGameProfileApi.getMojangServer(player_uuid.id)

    generated_image = await request_skinrendermc(
        player_profile.properties.textures.textures.SKIN.url,
        player_profile.properties.textures.textures.CAPE.url,
        player_uuid.name,
    )

    if generated_image:
        await app.send_message(
            group,
            MessageChain(
                [
                    generated_image,
                    Plain("\nvia SkinRenderMC, Mojang"),
                ]
            ),
        )
    else:
        await app.send_message(
            group,
            MessageChain([Plain(f"SkinRenderMC API Error")]),
        )


@channel.use(CommandSchema("&view.legacy {player_name: str}"))
async def legacy(app: Ariadne, group: Group, player_name: str):
    # TODO 屎一样，等待重写

    # 临时禁用 Hash 计算

    preview_images: List[Image] = list()
    # hashs = {"skin": None, "cape": None}
    for t_type in ["skin", "cape"]:
        legacy = await LegacyApi.get("https://littleskin.cn", player_name, t_type)
        if legacy.existed:
            # hashs[t_type] = legacy.sha256[:8]  # 截断为 8 位
            preview_images.append(Image(data_bytes=legacy.skin_preview))
    #     _message = f"""「{player_name}」
    # Skin Hash: {hashs.get('skin')}
    # Cape Hash: {hashs.get('cape')}"""
    await app.send_message(
        group,
        MessageChain(
            [
                *preview_images,
                # Plain(_message)
            ]
        ),
    )
