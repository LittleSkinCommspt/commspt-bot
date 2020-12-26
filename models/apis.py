from typing import Literal, Optional, Any
from pydantic import BaseModel


class CustomSkinLoaderLatestDownloads(BaseModel):
    Fabric: str
    Forge: str


class CustomSkinLoaderLatest(BaseModel):
    version: str
    downloads: CustomSkinLoaderLatestDownloads


class AuthlibInjectorLatestCheckSums(BaseModel):
    sha256: str


class AuthlibInjectorLatest(BaseModel):
    build_number: int
    version: str
    download_url: str
    checksums: AuthlibInjectorLatestCheckSums


class CustomSkinLoaderApiSkins(BaseModel):
    slim: Optional[str]
    default: Optional[str]


class CustomSkinLoaderApi(BaseModel):
    username: Optional[str]
    skins: Optional[CustomSkinLoaderApiSkins]
    cape: Optional[str]
    existed: bool = True
    skin_type: Literal['default', 'slim']

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.existed = bool(__pydantic_self__.username)
        __pydantic_self__.skins = 'default' if __pydantic_self__.skins.default else 'slim'
