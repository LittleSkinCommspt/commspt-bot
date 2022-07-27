import aiohttp
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, File
from graia.ariadne.model import Group
from graia.broadcast.builtin.decorators import Depend
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from utils.decorators import require_file, require_csl_log
from utils.csllogparser import cslHandler

channel = Channel.current()

@channel.use(ListenerSchema([GroupMessage], decorators=[Depend(require_file), Depend(require_csl_log)]))
async def parse_csl_log(app: Ariadne, group: Group, message: MessageChain):
    await app.send_message(group, MessageChain([Plain('正在解析日志...')]))
    # Get log file
    file: File = message[File][0]
    file_info = await app.get_file_info(group, file.id, with_download_info=True)
    download_url = file_info.download_info.url
    async with aiohttp.ClientSession() as session:
        async with session.get(download_url) as resp:
            csl_log = await resp.text()
    # Parse log
    env_info, playerInfoMessage, exceptionLines, csl_problems = cslHandler(csl_log)
    csl_problems_str = '\n'.join(csl_problems)
    await app.send_message(group, MessageChain(Plain(f'''{env_info}
{playerInfoMessage}
=== 抛出的异常 ===
{exceptionLines}
=== 检测到的错误 ===
{csl_problems_str}''')))
    
