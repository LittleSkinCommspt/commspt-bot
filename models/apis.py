import json
from base64 import b64decode
from datetime import date
from typing import Literal, Optional

import aiohttp
from pydantic import BaseModel, root_validator, validator


class CustomSkinLoaderLatest(BaseModel):
    class Downloads(BaseModel):
        Fabric: str
        Forge: str
    version: str
    downloads: Downloads

    @classmethod
    async def get(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://csl-1258131272.cos.ap-shanghai.myqcloud.com/latest.json') as resp:
                return cls.parse_raw(await resp.text())


class AuthlibInjectorLatest(BaseModel):
    class CheckSums(BaseModel):
        sha256: str
    build_number: int
    version: str
    download_url: str
    checksums: CheckSums

    @classmethod
    async def get(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://authlib-injector.yushi.moe/artifact/latest.json') as resp:
                return cls.parse_raw(await resp.text())


class CustomSkinLoaderApi(BaseModel):
    class Skins(BaseModel):
        slim: Optional[str]
        default: Optional[str]

    username: Optional[str]
    skins: Optional[Skins]
    cape: Optional[str]
    existed: bool = True
    skin_type: Optional[Literal['default', 'slim']] = 'default'

    @root_validator(pre=True)
    def extra_info(cls, values: dict):
        existed = 'username' in values and values['username'] != '404'
        if not existed or 'skins' not in values:
            skin_type = None
        else:
            skin_type = 'default' if 'default' not in values['skins'] else 'slim'
        values.update({
            'existed': existed,
            'skin_type': skin_type
        })
        return values

    @classmethod
    async def get(cls, api_root: str, username: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{api_root}/{username}.json') as resp:
                return cls.parse_raw(await resp.text())


class YggdrasilPlayerUuidApi(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    existed: bool = True

    @classmethod
    async def get(cls, api_root: str, username: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{api_root}/api/users/profiles/minecraft/{username}') as resp:
                if resp.status == 204:  # No content
                    return cls(existed=False)
                return cls.parse_raw(await resp.text())


class YggdrasilTextures(BaseModel):
    class Skin(BaseModel):
        class MetaData(BaseModel):
            model: Literal['default', 'slim']
        url: str
        metadata: Optional[MetaData]

    class Cape(BaseModel):
        url: str

    SKIN: Skin
    CAPE: Cape


class YggdrasilPropertiesTextures(BaseModel):
    timestamp: date
    profileId: str
    profileName: str
    textures: YggdrasilTextures


class YggdrasilGameProfileApi(BaseModel):
    class Properties(BaseModel):
        textures: YggdrasilPropertiesTextures
    id: str
    name: str
    properties: Properties  # a bit difference between API

    @root_validator(pre=True)
    def pre_process(cls, values):
        # Doc: https://wiki.vg/Mojang_API#UUID_-.3E_Profile_.2B_Skin.2FCape
        # base64 decode and a little change
        values['properties'][0]['textures'] = json.loads(b64decode(
            values['properties'][0]['value']))
        # array is useless while mojang is interesting
        values['properties'] = values['properties'][0]
        return values

    @classmethod
    async def get(cls, api_root: str, player_uuid: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{api_root}/sessionserver/session/minecraft/profile/{player_uuid}') as resp:
                return cls.parse_raw(await resp.text())
