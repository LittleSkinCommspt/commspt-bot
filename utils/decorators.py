from graia.ariadne.app import Ariadne
from graia.ariadne.model import Member, Group
from graia.ariadne.message.element import File
from graia.ariadne.message.chain import MessageChain
from graia.broadcast.exceptions import ExecutionStop
from settings import specialqq as qq


async def require_admin(app: Ariadne, member: Member):
    admins = await app.get_member_list(qq.notification_channel)
    admins_id = [m.id for m in admins]
    if member.id not in admins_id:
        raise ExecutionStop

async def require_file(message: MessageChain):
    if File not in message:
        raise ExecutionStop

async def require_csl_log(app: Ariadne, group: Group, message: MessageChain):
    file: File = message[File][0]
    file_info = await app.get_file_info(group, file.id)
    if file_info.name != 'CustomSkinLoader.log':
        raise ExecutionStop