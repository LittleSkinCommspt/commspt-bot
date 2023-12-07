from graia.ariadne.app import Ariadne
from graia.ariadne.event.mirai import MemberJoinRequestEvent
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.saya import Channel
from settings import specialqq as qq
from settings import verify_qmail_uid_api
import httpx
from loguru import logger
from utils.db_manager import write_uid_db

channel = Channel.current()


def get_answer_from_string(string: str) -> str | None:
    """
    Extracts a number from a string.

    Args:
        string (str): The input string.

    Returns:
        int | None: The extracted number if found, or None if not found.
    """
    # Split the string into lines and get the second line
    second_line = string.splitlines()[1]

    # Split the second line by "：" and get the second part
    answer = second_line.split("：", maxsplit=1)[1]

    # Remove leading and trailing whitespace from the answer
    return answer.strip()


def get_number_from_string(string: str) -> int | None:
    # Filter out all non-digit characters from the answer
    digits = "".join(filter(str.isdigit, get_answer_from_string(string)))

    # Convert the digits to an integer if any digits are found, otherwise return None
    return int(digits) if digits else None


@channel.use(ListenerSchema([MemberJoinRequestEvent]))
async def member_join_request(app: Ariadne, event: MemberJoinRequestEvent):
    if event.source_group not in [qq.littleskin_main]:
        return

    logger.info(
        f"MemberJoinRequestEvent: {event.supplicant} -> {event.source_group} / {event.group_name} : {event.message}"
    )
    uid_in_str = get_number_from_string(event.message)

    if not uid_in_str:
        return

    # write into database
    await write_uid_db(uid_in_str, event.supplicant)

    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(
            verify_qmail_uid_api, params={"uid": uid_in_str, "qq": event.supplicant}
        )

    if response.status_code == httpx.codes.OK:
        event.accept()
        logger.info("MemberJoinRequestEvent: ACCEPTED by bot")
    else:
        logger.info("MemberJoinRequestEvent: IGNORED")
