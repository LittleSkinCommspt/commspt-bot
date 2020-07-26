import requests
import base64
from mirai import Plain
import json


class YggdrasilProfile():
    class skin:
        pass

    class cape:
        pass

    def __init__(self, yggdrasil_profile: dict):
        self.uuid = yggdrasil_profile['profileId']
        self.name = yggdrasil_profile['profileName']

        if 'SKIN' in yggdrasil_profile['textures']:
            self.skin.model = 'slim' if 'metadata' in yggdrasil_profile['textures']['SKIN'] else 'default'
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

    def getCsl(self) -> Plain:
        r = requests.get(
            f'https://mcskin.littleservice.cn/csl/{self.playerName}.json')
        j = r.json()
        name = j['username']
        if name != '404':
            skin_type = 'default' if 'default' in j['skins'] else 'slim'
            skin_hash = j['skins'][skin_type] if j['skins'][skin_type] else '无'
            cape_hash = j['cape'] if j['cape'] else '无'
            return Plain(text=f'''角色名：{name}
模型：{skin_type}
皮肤：{skin_hash}
披风：{cape_hash}''')
        else:
            return Plain(text='[Error] 找不到角色')

    def getYgg(self) -> Plain:
        r1 = requests.post(
            'https://mcskin.littleservice.cn/api/yggdrasil/api/profiles/minecraft', json=[self.playerName])
        s1 = r1.json()
        if s1 == []:
            return Plain(text='[Error] 找不到角色')
        #
        player_uuid = s1[0]['id']
        r2 = requests.get(
            f'https://mcskin.littleservice.cn/api/yggdrasil/sessionserver/session/minecraft/profile/{player_uuid}')
        s2 = r2.json()
        unbase64ed = s2['properties'][0]['value']
        _gameprofile = base64.b64decode(unbase64ed)
        #
        print(json.loads(_gameprofile))
        gameprofile = YggdrasilProfile(json.loads(_gameprofile))
        return Plain(text=f'''角色名：{gameprofile.name}
UUID：{gameprofile.uuid}
模型：{gameprofile.skin.model}
皮肤：{gameprofile.skin.hash} ({gameprofile.skin.provider})
披风：{gameprofile.cape.hash} ({gameprofile.cape.provider})''')
