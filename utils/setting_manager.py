from pydantic import BaseSettings, BaseModel


class DefinedQQ(BaseModel):
    constance: int
    littleskin_main: int
    littleskin_cafe: int
    commspt_group: int
    csl_group: int
    notification_channel: int
    dev_group: int


class Connection(BaseModel):
    account: int
    token: str
    ws_endpoint: str


class API_SkinRenderMC(BaseModel):
    endpoint: str


class API_mihari_svg(BaseModel):
    endpoint: str

class DB_mongo(BaseModel):
    url: str

class Setting(BaseSettings):
    command_prompt: str = "&"
    defined_qq: DefinedQQ
    connection: Connection
    api_skinrendermc: API_SkinRenderMC
    api_mihari_svg: API_mihari_svg
    db_mongo: DB_mongo

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = '__'


SETTING = Setting()