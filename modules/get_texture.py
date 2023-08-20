from uuid import UUID

from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Group
from graia.saya import Channel

from models.apis import CustomSkinLoaderApi

from yggdrasil_mc import YggdrasilPlayer
from yggdrasil_mc.model import YggdrasilTexturesModel

channel = Channel.current()


@channel.use(CommandSchema("&csl {player_name: str}"))
async def csl(app: Ariadne, group: Group, player_name: str):
    result = await CustomSkinLoaderApi.get("https://littleskin.cn/csl", player_name)
    if not result.player_existed:
        _message = f"「{player_name}」不存在"
    else:
        _message = f"""「{player_name}」
Skin: {result.skin_hash[:8] if result.skin_existed else None} [{result.skin_type if result.skin_existed else None}]
Cape: {result.cape_hash[:8] if result.cape_existed else None}"""
    await app.send_message(group, MessageChain([Plain(_message)]))


@channel.use(CommandSchema("&ygg {player_name: str}"))
async def ygg(app: Ariadne, group: Group, player_name: str):
    littleskin_yggdrasil_root = "https://littleskin.cn/api/yggdrasil"
    ygg_server = YggdrasilPlayer(littleskin_yggdrasil_root)
    player_uuid = await ygg_server.Uuid.get3rdAsync(player_name)
    if not player_uuid.existed:
        _message = f"「{player_name}」不存在"
    else:
        result = await ygg_server.Profile.get3rdAsync(player_uuid.id)
        textures = result.properties.textures.textures
        _message = f"""「{result.name}」
Skin: {textures.skin.hash[:8] if textures.skin.url else None} [{textures.skin.metadata.model if textures.skin else None}]
Cape: {textures.cape.hash[:8] if textures.cape.url else None}
UUID: {UUID(player_uuid.id)}"""
    await app.send_message(group, MessageChain([Plain(_message)]))


def is_existed(value: bool) -> str:
    """Check if a value exists or not.

    Args:
        value (bool): The value to check.

    Returns:
        str: "存在" if the value is True, "不存在" otherwise.
    """
    return "存在" if value else "不存在"


@channel.use(CommandSchema("&check {player_name: str}"))
async def check(app: Ariadne, group: Group, player_name: str):
    _message: list[str] = [f"「{player_name}」的报告"]

    csl_texture = await CustomSkinLoaderApi.get(
        "https://littleskin.cn/csl", player_name
    )

    ygg_server = YggdrasilPlayer("https://littleskin.cn/api/yggdrasil")
    ygg_uuid_result = await ygg_server.Uuid.get3rdAsync(player_name)

    if not csl_texture.player_existed == ygg_uuid_result.existed:
        await app.send_message(
            group,
            MessageChain(
                [
                    Plain(f"{_message[0]}\n"),
                    Plain(
                        f"- 此角色在 CSL API 上{is_existed(ygg_uuid_result.existed)}，在 YGG API 上却{is_existed(csl_texture.player_existed)}！"
                    ),
                ]
            ),
        )
        return

    if not ygg_uuid_result.existed and not csl_texture.player_existed:
        await app.send_message(
            group,
            MessageChain(
                [Plain(f"{_message[0]}\n"), Plain(f"- 此角色在 LittleSkin 中未被找到！")]
            ),
        )
        return

    # check textures
    ygg_texture = await ygg_server.Profile.get3rdAsync(ygg_uuid_result.id)

    # - skin
    if csl_texture.skin_hash != ygg_texture.properties.textures.textures.skin.hash:
        _message.append("- Skin Hash 不一致！")

    # - cape
    if csl_texture.cape_hash != ygg_texture.properties.textures.textures.cape.hash:
        _message.append("- Cape Hash 不一致！")

    if len(_message) == 1:
        _message.append("- 一致性检查通过。")
    else:
        _message.append("- 一致性检查失败！")
    
    # check mojang
    ygg_mojang = YggdrasilPlayer()
    ygg_mojang_uuid_result = await ygg_mojang.Uuid.getMojangAsync(player_name)

    if ygg_mojang_uuid_result.existed:
        _message.append("- 在 Mojang 中存在同名角色！")
    else:
        _message.append("- 在 Mojang 中不存在同名角色。")

    await app.send_message(group, MessageChain([Plain("\n".join(_message))]))
