import json
from base64 import b64decode
from datetime import date
from typing import Literal, Optional, Union
from enum import Enum
import hashlib
from io import BytesIO

import aiohttp
from pydantic import BaseModel, root_validator, validator
from pydantic.fields import Field


class CustomSkinLoaderLatest(BaseModel):
    class Downloads(BaseModel):
        Fabric: str
        Forge: str  # Legacy, 1.16.5-
        ForgeActive: str  # New, 1.17+

    version: str
    downloads: Downloads

    @classmethod
    async def get(cls):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://csl-1258131272.cos.ap-shanghai.myqcloud.com/latest.json"
            ) as resp:
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
            async with session.get(
                "https://authlib-injector.yushi.moe/artifact/latest.json"
            ) as resp:
                return cls.parse_raw(await resp.text())


class CustomSkinLoaderApi(BaseModel):
    class Skins(BaseModel):
        slim: Optional[str]
        default: Optional[str]

    username: Optional[str]
    skins: Optional[Skins]
    skin_hash: Optional[str] = ""
    cape_hash: Optional[str] = Field("", alias="cape")
    player_existed: Optional[bool] = True
    skin_type: Optional[Literal["default", "slim", None]] = None
    skin_existed: Optional[bool] = True
    cape_existed: Optional[bool] = True

    @root_validator(pre=True)
    def pre_processor(cls, values: dict):
        #
        player_existed = bool(values)
        if not player_existed:
            skin_type = None
            skin_existed = False
            cape_existed = False
        else:
            skin_type = (
                "slim"
                if "slim" in values["skins"]
                else "default"
                if values["skins"]["default"]
                else None
            )
            cape_existed = "cape" in values and bool(values["cape"])
        # parse skin hash
        if skin_type == "default":
            skin_hash = values["skins"]["default"]
            skin_existed = True
        elif skin_type == "slim":
            skin_hash = values["skins"]["slim"]
            skin_existed = True
        else:
            skin_hash = None
            skin_existed = False

        values.update(
            {
                "player_existed": player_existed,
                "skin_type": skin_type,
                "skin_existed": skin_existed,
                "cape_existed": cape_existed,
                "skin_hash": skin_hash,
            }
        )
        return values

    @classmethod
    async def get(cls, api_root: str, username: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{api_root}/{username}.json") as resp:
                return cls.parse_raw(await resp.text())


class YggdrasilPlayerUuidApi(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    existed: bool = True

    @classmethod
    async def get(cls, api_root: str, username: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{api_root}/api/users/profiles/minecraft/{username}"
            ) as resp:
                if resp.status == 204:  # No content
                    return cls(existed=False)
                return cls.parse_raw(await resp.text())


def make_hash(cls, values):
    url = values["url"]
    last_slash_location = url.rindex("/")
    real_hash = url[last_slash_location + 1 :]
    values["hash"] = real_hash
    return values


class YggdrasilTextures(BaseModel):
    class Skin(BaseModel):
        class MetaData(BaseModel):
            model: Literal["default", "slim"] = "default"

        url: Optional[str]
        hash: Optional[str] = None
        metadata: Optional[MetaData] = MetaData(model="default")
        _hash = root_validator(pre=True, allow_reuse=True)(make_hash)

    class Cape(BaseModel):
        url: Optional[str]
        hash: Optional[str] = None
        _hash = root_validator(pre=True, allow_reuse=True)(make_hash)

    SKIN: Optional[Skin]
    CAPE: Optional[Cape]


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
    def pre_processer(cls, values):
        # Doc: https://wiki.vg/Mojang_API#UUID_-.3E_Profile_.2B_Skin.2FCape
        # base64 decode and a little change
        values["properties"][0]["textures"] = json.loads(
            b64decode(values["properties"][0]["value"])
        )
        # array is useless while mojang is interesting
        values["properties"] = values["properties"][0]
        return values

    @classmethod
    async def get(cls, api_root: str, player_uuid: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{api_root}/sessionserver/session/minecraft/profile/{player_uuid}"
            ) as resp:
                return cls.parse_raw(await resp.text())


async def getTexturePreview(blessing_skin_root: str, texture_hash: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{blessing_skin_root}/preview/hash/{texture_hash}?png"
        ) as resp:
            if resp.status == 404:
                return
            else:
                return await resp.content.read()


class MojangPlayerUuidApi(YggdrasilPlayerUuidApi):
    @classmethod
    async def get(cls, username: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.mojang.com/users/profiles/minecraft/{username}"
            ) as resp:
                if resp.status == 204:  # No content
                    return cls(existed=False)
                return cls.parse_raw(await resp.text())


class LegacyApi(BaseModel):
    image_bytes: Optional[bytes] = None
    sha256: Optional[str] = None
    skin_preview: Optional[bytes] = None
    texture_type: str
    existed: bool = True

    @classmethod
    async def get(cls, api_root: str, username: str, texture_type: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{api_root}/{texture_type}/{username}.png") as resp:
                if resp.status == 404:
                    return cls(texture_type=texture_type, existed=False)
                else:
                    image_bytes = await resp.content.read()
                    sha256 = hashlib.sha256(image_bytes).hexdigest()
                    return cls(
                        image_bytes=image_bytes,
                        sha256=sha256,
                        skin_preview=await getTexturePreview(api_root, sha256),
                        texture_type=texture_type,
                    )
