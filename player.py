import requests
import base64
from mirai import Plain


def getCslPlayerInfo(player_name: str):
    if not player_name:
        return Plain(text='[Error] 缺少实参 player_name')
    r = requests.get(f'https://mcskin.littleservice.cn/csl/{player_name}.json')
    j = r.json()
    name = j['username']
    if name != '404':
        skin_type = 'default' if 'default' in j['skins'] else 'slim'
        skin_hash = j['skins'][skin_type]
        cape_hash = j['cape'] if 'cape' in j else '无'
        return Plain(text=f'''角色名：{name}
模型：{skin_type}
皮肤：{skin_hash}
披风：{cape_hash}''')
    else:
        return Plain(text='[Error] 找不到角色')

def getYggPlayerInfo(player_name: str):
    if not player_name:
        return Plain(text='[Error] 缺少实参 player_name')

    r1 = requests.post(
        'https://mcskin.littleservice.cn/api/yggdrasil/api/profiles/minecraft', json=[player_name])
    s1 = r1.json()
    if s1 == []:
        return Plain(text='[Error] 找不到角色')
    # 
    player_uuid = s1[0]['id']
    r2 = requests.get(
        f'https://mcskin.littleservice.cn/api/yggdrasil/sessionserver/session/minecraft/profile/{player_uuid}')
    s2 = r2.json()
    unbase64ed = s2['properties'][0]['value']
    i = base64.b64decode(unbase64ed)
    return Plain(text=i)


def showCslLog():
    return Plain(text='CustomSkinLoader 的日志位于 .minecraft/CustomSkinLoader/CustomSkinLoader.log，请将此文件直接上传至群文件')
