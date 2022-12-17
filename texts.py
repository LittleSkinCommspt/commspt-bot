from typing import List


class TextFields(object):
    '''储存有文本字段'''
    ping = 'Pong'
    new_question_nofication = '有用户提出了一个新的问题，请尽快进行解答。'
    new_question_sent = '已收到你的问题，请耐心等待答复。'
    csl_gui = '新的 CustomSkinLoader GUI 地址是 https://mc-csl.netlify.app/ 。'
    help = '请查看 https://bot-manual.restent.win/'
    manual = '\n请仔细阅读 LittleSkin 用户使用手册，特别是「常见问题解答」！\nhttps://manual.littlesk.in/'
    ot = '\n请停止讨论与 LittleSkin 无关的话题并前往群 651672723。\n大水怪将会收到我们赠送的禁言大礼包。'
    ygg_server_jvm = '请在启动脚本中加入参数 -Dauthlibinjector.debug=all，然后将 logs/latest.log 上传至群文件'
    domain = '我们推测您可能使用百度搜索 LittleSkin 并使用了在中国大陆过时的域名，我们建议您：\n1.将域名替换成 littlesk.in；\n2.使用除百度外的搜索引擎。'
    view_hash_length_error = 'Hash 长度有误'
    view_not_200_error = '找不到材质？'
    view_no_hash_error = '请提供材质 Hash'
    mail = '请发送邮件至 support@littlesk.in，并在邮件中详细说明你的情况\n更多：https://manual.littlesk.in/email.html'
    csl_log = 'CustomSkinLoader 的日志通常位于 .minecraft/CustomSkinLoader/CustomSkinLoader.log，请将文件直接发送至群内。'
    csl_config_littleskin = '''
    若安装了csl后无法正确加载皮肤，可能是ID存在同名正版被优先加载，可使用以下方法
手动修改csl加载顺序

https://manual.littlesk.in/newbee/mod.html
————————————————
您可以在「群文件-资源下载」下载到一个 CustomSkinLoader.json 文件，将其直接替换游戏 csl 目录下的文件即可
    '''
    csl_config_csl_group = '请访问 https://csl.littleservice.cn/faq/config-csl.html 以了解如何修改 CustomSkinLoader 的配置文件'
    clfcsl = '''在 1.7.10 中使用需要同时安装最新 Forge 版的 CustomSkinLoader 和 CompatibilityLayerForCustomSkinLoader，
你可以在 https://www.mcbbs.net/thread-1109996-1-1.html 下载到后者'''
    browser = '''请仔细阅读图片中的内容！以下是几个推荐的浏览器
Chrome: https://www.google.cn/chrome
Firefox: https://www.mozilla.org/firefox/new/
Edge: https://aka.ms/msedge'''
    ygg_nsis = '''请确认服务器正确配置 authlib-injector 并将 online-mode 设为 true，否则请使用 CustomSkinLoader。
更多：https://manual.littlesk.in/advanced/yggdrasil.html'''
    client_refresh = '请在你的 启动器 -> 账户列表 内刷新你的账户（以 HMCL3 为例）'
    csl_log_parsing = 'Got it! I\'m busy with parsing it now!'
    join_welcome = '欢迎来到 LittleSkin 问题反馈群！\n提问前请先仔细阅读群内置顶公告，如因未阅读而导致的问题可能不会被回答或被禁言。'
    pay_for_help = '在群里和大佬吹牛逼帮助不了你的问题？\nhttps://afdian.net/@tnqzh123 \n购买一对一帮助服务即可快速解决你的问题！'
    question_keywords: List[str] = ['为什么', '怎么回事', '为啥', '问个问题', '请问', '问一下', '如何解决',
                                    '我想问', '什么问题', '咋回事', '怎么办', '怎么解决']
    question_keywords_excepted: List[str] = ['为什么要', '怎么能', '怎么这样', '干嘛', '干吗', '怎么可以', '难道']    
    log_minecraft = '请使用启动器的「测试游戏」功能启动游戏，并在复现问题后导出日志发送至群内。如果问题与外置登录有关，请在启动器的「JVM 参数（Java 虚拟机参数）」设置中填入 -Dauthlibinjector.debug'
    log_launcher = '请在启动器中复现你的问题，然后导出启动器日志发送至群内'
    java8_latest = '''请更新到最新的 Java 8 版本，将下面链接复制到浏览器中下载
Windows x64: https://honoka.eu.org/java8/win64
Windows x32: https://honoka.eu.org/java8/win32
macOS: https://honoka.eu.org/java8/macos
同时为了确保启动游戏时能够引导到正确的 Java 8 版本，我们建议您卸载其他 Java 8 版本'''
    java_latest = '''请更新到最新的 Java 17 版本，将下面链接复制到浏览器中下载
Windows x64: https://honoka.eu.org/java/win64
Windows x32: https://honoka.eu.org/java/win32
macOS: https://honoka.eu.org/java/macos
同时为了确保启动游戏时能够引导到正确的 Java 17 版本，我们建议您卸载其他 Java 17 版本'''
    hmcl_latest = '''请到 HMCL 官网下载最新版本的 HMCL
https://hmcl.huangyuhui.net/download/'''
    ms_oauth = '''通过微软邮箱直接授权登录的用户初始没有密码，请在 LittleSkin 里先退出登录，然后在登录界面点击忘记密码，即可通过邮箱修改密码。'''
    cape_format = '''「不是有效的披风文件」
LittleSkin 对于披风文件的格式要求如下：
·png 格式文件；
·宽高比需为 2:1；
·为 64x32 的整倍数。'''
    pro_verify = '''目前在 LittleSkin 验证正版后有以下功能：
·在主页上获得一个「正版」（英文为“Pro”）徽标
·赠送您 1k 积分；
·在皮肤站内取回您的正版 ID 对应的角色（如果您的 ID 已被人抢注）。
请注意，正版验证过后，您的 LittleSkin 外置登录账号并不具备正版的属性，性质仍为离线账号，您无法将 LittleSkin 外置登录账号代替正版账号使用。'''
    network = '''「登录失败：身份验证服务器目前正在停机维护」
「无法验证用户名」
「验证服务器他们宕了吗？」：
由于各种玄学的网络问题导致此问题随机出现，当你看到这条消息由社区技术支持人员触发时说明 LittleSkin 并没有出现宕机等问题，请优先检查您的网络环境和使用的域名是否为 littleskin.cn，并在重启游戏后再次尝试登录。
（总之这不是 LittleSkin 的问题）'''
    cafe = '''欢迎加入 Honoka Café 穗香咖啡馆来水群～\n群号 651672723。'''
