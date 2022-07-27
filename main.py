import pkgutil

from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.message.commander import Commander
from graia.broadcast import Broadcast
from graia.saya import Saya

import settings

# 初始化
broadcast = create(Broadcast)
app = Ariadne(connection=settings.Connection)
cmd = create(Commander)
saya = create(Saya)

with saya.module_context():
    for module_info in pkgutil.iter_modules(['modules']):
        print(f'Loading {module_info.name}')
        saya.require(f'modules.{module_info.name}')


if __name__ == '__main__':
    app.launch_blocking()
