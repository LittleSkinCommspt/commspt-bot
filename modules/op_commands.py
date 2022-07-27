from typing import List, Tuple

from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.element import At, Plain, Quote, Source
from graia.ariadne.model import Group, Member
from graia.broadcast.builtin.decorators import Depend
from graia.broadcast.exceptions import ExecutionStop
from graia.saya import Channel
from settings import specialqq as qq
from texts import TextFields as tF
from utils.permissons import require_admin

channel = Channel.current()



@channel.use(CommandSchema('&recall', decorators=[Depend(require_admin)]))
async def recall(app: Ariadne, message: MessageChain):
    if Quote in message:
        origin_message = message[Quote][0].id
        current_message = message[Source][0].id
        await app.recall_message(origin_message)
        await app.recall_message(current_message)


@channel.use(CommandSchema('&mute {time: int = 10} {...targets: At}', decorators=[Depend(require_admin)]))
async def mute(app: Ariadne, group: Group, time: int, targets: Tuple[At]):
    targets = [m.target for m in targets]
    for target in targets:
        await app.mute_member(group, target, time * 60)


@channel.use(CommandSchema('&unmute {...targets: At}', decorators=[Depend(require_admin)]))
async def unmute(app: Ariadne, group: Group, targets: Tuple[At]):
    targets = [m.target for m in targets]
    for target in targets:
        await app.unmute_member(group, target) 
