import arrow
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

from yggdrasil_mc import YggdrasilPlayer
from utils import skinrendermcapi

channel = Channel.current()


@channel.use(CommandSchema("&view.csl {player_name: str}"))
async def customskinloader(app: Ariadne, group: Group, player_name: str):
    result = await CustomSkinLoaderApi.get("https://littleskin.cn/csl", player_name)
    if not result.player_existed:
        await app.send_message(group, MessageChain([Plain(f"「{player_name}」不存在")]))
    else:
        bs_root = "https://littleskin.cn"
        preview_images: list[Image] = list()
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

via Blessing Skin, CustomSkinLoader API"""
                    ),
                ]
            ),
        )


@channel.use(CommandSchema("&view.ygg {player_name: str}"))
async def yggdrasil(app: Ariadne, group: Group, player_name: str):
    littleskin_yggdrasil_root = "https://littleskin.cn/api/yggdrasil"
    ygg_server = YggdrasilPlayer(littleskin_yggdrasil_root)
    player_uuid = await ygg_server.Uuid.get3rdAsync(player_name)
    if not player_uuid.existed:
        _message = f"「{player_name}」不存在"
        await app.send_message(group, MessageChain([Plain(_message)]))
        return
    else:
        result = await ygg_server.Profile.get3rdAsync(player_uuid.id)

    generated_image = await skinrendermcapi.request_skinrendermc(
        result.properties.textures.textures.skin.url,
        result.properties.textures.textures.cape.url,
        player_uuid.name,
    )

    if generated_image:
        await app.send_message(
            group,
            MessageChain(
                [
                    Image(
                        data_bytes=skinrendermcapi.process_image(
                            generated_image,
                            f"{arrow.now()}, via SkinRenderMC, LittleSkin",
                        )
                    )
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
    ygg_server = YggdrasilPlayer()
    player_uuid = await ygg_server.Uuid.getMojangAsync(player_name)
    if not player_uuid.existed:
        _message = f"「{player_name}」不存在"
        await app.send_message(group, MessageChain([Plain(_message)]))
        return
    else:
        result = await ygg_server.Profile.getMojangAsync(player_uuid.id)

    generated_image = await skinrendermcapi.request_skinrendermc(
        result.properties.textures.textures.skin.url,
        result.properties.textures.textures.cape.url,
        player_uuid.name,
    )

    if generated_image:
        await app.send_message(
            group,
            MessageChain(
                [
                    Image(
                        data_bytes=skinrendermcapi.process_image(
                            generated_image, f"{arrow.now()}, via SkinRenderMC, Mojang"
                        )
                    )
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

    preview_images: list[Image] = list()
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
