from uuid import UUID
import arrow

from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.element import Plain, Image
from graia.ariadne.model import Group
from graia.saya import Channel


from yggdrasil_mc import YggdrasilPlayer
from utils import mihariapi

channel = Channel.current()


@channel.use(CommandSchema("&player {player_name: str}"))
async def ygg_ng(app: Ariadne, group: Group, player_name: str):
    littleskin_yggdrasil_root = "https://littleskin.cn/api/yggdrasil"
    ygg_server = YggdrasilPlayer(littleskin_yggdrasil_root)
    player_uuid = await ygg_server.Uuid.get3rdAsync(player_name)
    if not player_uuid.existed:
        _message = f"「{player_name}」不存在"
        await app.send_message(group, MessageChain([Plain(_message)]))
    else:
        result = await ygg_server.Profile.get3rdAsync(player_uuid.id)
        textures = result.properties.textures.textures
    await app.send_message(
        group,
        MessageChain(
            [
                Image(
                    data_bytes=await mihariapi.render_image(
                        open("assets/player-profile.svg", "rb"),
                        {
                            "time": str(arrow.now()),
                            "player_name": result.name,
                            "skin_type": textures.skin.metadata.model if textures.skin else "/",
                            "skin_hash": textures.skin.hash[:8] if textures.skin.url else "/",
                            "has_cape": "yes" if textures.cape.url else "no",
                            "cape_hash": textures.cape.hash[:8] if textures.cape.url else "/",
                        }
                    )
                )
            ]
        ),
    )
