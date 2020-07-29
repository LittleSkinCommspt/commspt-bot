import requests
import base64
import io
from mirai import Plain, Image
# from PIL import Image as pilImage
import json


class YggdrasilProfile():
    class skin:
        '''皮肤'''
        pass

    class cape:
        '''披风'''
        pass

    def __init__(self, yggdrasil_profile: dict):
        self.uuid = yggdrasil_profile['profileId']
        self.name = yggdrasil_profile['profileName']

        if 'SKIN' in yggdrasil_profile['textures']:
            self.skin.model = 'slim' if 'metadata' in yggdrasil_profile[
                'textures']['SKIN'] else 'default'
            self.skin.url = yggdrasil_profile['textures']['SKIN']['url']
            self.skin.hash = self.getHashFromUrl(self.skin.url)
            self.skin.provider = self.getTextureProvider(self.skin.url)
        else:
            self.skin.model = None
            self.skin.url = None
            self.skin.hash = None
            self.skin.provider = None

        if 'CAPE' in yggdrasil_profile['textures']:
            self.cape.url = yggdrasil_profile['textures']['CAPE']['url']
            self.cape.provider = self.getTextureProvider(self.cape.url)
            self.cape.hash = self.getHashFromUrl(self.cape.url)
        else:
            self.cape.url = None
            self.cape.provider = None
            self.cape.hash = None

    @staticmethod
    def getHashFromUrl(url: str) -> str:
        _hash = url.split('/')[-1]
        return _hash

    @staticmethod
    def getTextureProvider(url: str) -> str:
        _provider = 'LittleSkin' if 'mcskin.littleservice.cn' in url else 'Mojang'
        return _provider


class PlayerProfile():
    def __init__(self, player_name: str):
        self.playerName = player_name

    @staticmethod
    def getPreviewByHash(texture_hash: str) -> Image:
        '''通过 hash 获取 Image 对象'''
        r = requests.get(
            f'https://mcskin.littleservice.cn/preview/hash/{texture_hash}?png')
        # WebP 转 PNG
        # webpIo = io.BytesIO(r.content)
        # pngIo = io.BytesIO()
        # middleImage = pilImage.open(webpIo)
        # middleImage.save(pngIo, format='PNG')

        if r.status_code == 200:
            return Image.fromBytes(r.content)
        else:
            return None

    def previewImage(self, skin_hash: str, cape_hash: str) -> list:
        '''获取皮肤和披风的预览图

        使用：*self.previewImage(skin_hash, cape_hash)'''
        _l = list()
        if skin_hash:
            _l.append(self.getPreviewByHash(skin_hash))
        if cape_hash:
            _l.append(self.getPreviewByHash(cape_hash))
        return _l

    def getCsl(self) -> list:
        r = requests.get(
            f'https://mcskin.littleservice.cn/csl/{self.playerName}.json')
        j = r.json()
        name = j['username']
        if name != '404':
            skin_type = 'default' if 'default' in j['skins'] else 'slim'
            skin_hash = j['skins'][skin_type] if j['skins'][skin_type] else None
            cape_hash = j['cape'] if j['cape'] else None
            return [Plain(text=f'''角色名：{name}
模型：{skin_type}
皮肤：{skin_hash}
披风：{cape_hash}
'''), *self.previewImage(skin_hash, cape_hash)]
        else:
            return [Plain(text='[Error] 找不到角色')]

    def getYgg(self) -> list:
        r1 = requests.post(
            'https://mcskin.littleservice.cn/api/yggdrasil/api/profiles/minecraft', json=[self.playerName])
        s1 = r1.json()
        if s1 == []:
            return [Plain(text='[Error] 找不到角色')]
        #
        player_uuid = s1[0]['id']
        r2 = requests.get(
            f'https://mcskin.littleservice.cn/api/yggdrasil/sessionserver/session/minecraft/profile/{player_uuid}')
        s2 = r2.json()
        unbase64ed = s2['properties'][0]['value']
        _gameprofile = base64.b64decode(unbase64ed)

        #
        gameprofile = YggdrasilProfile(json.loads(_gameprofile))
        return [Plain(text=f'''角色名：{gameprofile.name}
UUID：{gameprofile.uuid}
模型：{gameprofile.skin.model}
皮肤：{gameprofile.skin.hash} ({gameprofile.skin.provider})
披风：{gameprofile.cape.hash} ({gameprofile.cape.provider})
'''), *self.previewImage(gameprofile.skin.hash if gameprofile.skin.provider == 'LittleSkin' else None,
                         gameprofile.cape.hash if gameprofile.cape.provider == 'LittleSkin' else None)]
