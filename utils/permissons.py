from graia.ariadne.app import Ariadne
from graia.ariadne.model import Member
from graia.broadcast.exceptions import ExecutionStop
from settings import specialqq as qq


async def require_admin(app: Ariadne, member: Member):
    admins = await app.get_member_list(qq.notification_channel)
    admins_id = [m.id for m in admins]
    if member.id not in admins_id:
        raise ExecutionStop
