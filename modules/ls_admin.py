from typing import Tuple

from graia.ariadne.app import Ariadne
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At
from graia.ariadne.model import Group
from graia.saya import Channel

from utils.db_manager import get_uid

channel = Channel.current()


@channel.use(CommandSchema('&uid {...targets: At}'))
async def uid(app: Ariadne, group: Group, targets: Tuple[At]):
    rep: list[str] = list()
    for t in targets:
        m = await app.get_member(group, t.target)
        uid = await get_uid(t.target)
        rep.append(f"<{t.target}>[{m.name}]: {uid}")

    await app.send_message(group, MessageChain("\n".join(rep)))
    
