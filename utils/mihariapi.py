import httpx
from typing import IO, Mapping
import json


async def render_image(svg: IO, params: Mapping[str, str]) -> bytes:
    async with httpx.AsyncClient(http2=True, timeout=10) as client:
        r = await client.post(
            "http://10.50.0.4:57681/png/template",
            params={"dpi": 300},
            data={"params": json.dumps(params)},
            files={"file": svg},
        )
        return r.content
