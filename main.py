import pkgutil

from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.message.commander import Commander
from graia.broadcast import Broadcast
from graia.saya import Saya

import settings

# 初始化
broadcast = create(Broadcast)
app = Ariadne(connection=settings.Connection)
cmd = create(Commander)
saya = create(Saya)

with saya.module_context():
    for module_info in pkgutil.iter_modules(['modules']):
        print(f'Loading {module_info.name}')
        saya.require(f'modules.{module_info.name}')




# @broadcast.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([CommandMatch('view')], {"params": WildcardMatch(optional=True)}))])
# async def command_handler(app: Ariadne, group: Group, params: WildcardMatch):
#     player_name = params.result.asDisplay()
#     result = await apis.CustomSkinLoaderApi.get('https://littleskin.cn/csl', player_name)
#     if not result.player_existed:
#         await app.sendGroupMessage(group, MessageChain.create([Plain(f'「{player_name}」不存在')]))
#     else:
#         bs_root = 'https://littleskin.cn'
#         preview_images: List[Image] = list()
#         for texture in [result.skin_hash, result.cape_hash]:
#             if texture:
#                 preview_images.append(Image(data_bytes=await apis.getTexturePreview(
#                     bs_root, texture)))
#     await app.sendGroupMessage(group,
#                                MessageChain.create([*preview_images,
#                                                     Plain(f'''「{player_name}」
# Skin: {result.skin_hash[:7]} [{result.skin_type}]
# Cape: {result.cape_hash[:7] if result.cape_existed else None}''')]))


# @broadcast.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([CommandMatch('view.mojang')], {"params": WildcardMatch(optional=True)}))])
# async def command_handler(app: Ariadne, group: Group, params: WildcardMatch):




if __name__ == '__main__':
    app.launch_blocking()
