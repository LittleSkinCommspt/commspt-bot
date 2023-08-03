from urllib import response
from graia.ariadne.app import Ariadne
from graia.ariadne.event.mirai import MemberJoinRequestEvent
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya import Channel
from settings import specialqq as qq
from settings import verify_qmail_uid_api
import httpx
from loguru import logger

channel = Channel.current()

def get_number_from_string(string: str) -> int | None:
    """
    Extracts and returns the digits found in the given string.
    
    Args:
        string (str): The input string.
    
    Returns:
        int: The number extracted from the string, or None if no digits are found.
    """
    digits = ''.join(filter(str.isdigit, string))
    return int(digits) if digits else None

@channel.use(ListenerSchema([MemberJoinRequestEvent]))
async def member_join_request(app: Ariadne, event: MemberJoinRequestEvent):
    if event.source_group not in [qq.littleskin_main]:
        return

    logger.info(f"MemberJoinRequestEvent: {event.supplicant} -> {event.source_group} / {event.group_name} : {event.message}")
    uid_in_str = get_number_from_string(event.message)

    if not uid_in_str:
        return
    
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(verify_qmail_uid_api, params={"uid": uid_in_str, "qq": event.supplicant})
    
    if response.status_code == httpx.codes.OK:
        event.accept()
        logger.info("MemberJoinRequestEvent: ACCEPTED by bot")
    else:
        logger.info("MemberJoinRequestEvent: IGNORED")

