from typing import Tuple

from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.commander.saya import CommandSchema
from graia.ariadne.message.element import At, Plain, Quote, Source
from graia.ariadne.model import Group, Member
from graia.broadcast.builtin.decorators import Depend
from graia.saya import Channel
from utils.permissons import require_admin

channel = Channel.current()



@channel.use(CommandSchema('&recall', decorators=[Depend(require_admin)]))
async def recall(app: Ariadne, message: MessageChain):
    if Quote in message:
        origin_message = message[Quote][0].id
        current_message = message[Source][0].id
        await app.recall_message(origin_message)
        await app.recall_message(current_message)


@channel.use(CommandSchema('&mute {...targets: At}', decorators=[Depend(require_admin)]))
async def mute(app: Ariadne, group: Group, targets: Tuple[At]):
    targets = [m.target for m in targets]
    for target in targets:
        await app.mute_member(group, target, 10 * 60)


@channel.use(CommandSchema('&unmute {...targets: At}', decorators=[Depend(require_admin)]))
async def unmute(app: Ariadne, group: Group, targets: Tuple[At]):
    targets = [m.target for m in targets]
    for target in targets:
        await app.unmute_member(group, target) 
