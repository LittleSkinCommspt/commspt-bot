from typing import List


class TextFields(object):
    '''储存有文本字段'''
    ping = 'Pong'
    new_question_nofication = 'LittleSkin 用户交流群内有一个新的问题已被提出。'
    new_question_sent = '运营组及社区技术支持组已收到你的问题，请耐心等待答复。'
    csl_gui = '新的 CustomSkinLoader GUI 地址是 https://mc-csl.netlify.app/ 。'
    help = '请查看 https://bot-manual.restent.win/'
    manual = '\n请仔细阅读 LittleSkin 用户使用手册，特别是「常见问题解答」！\nhttps://manual.littlesk.in/'
    ot = '\n您正在讨论无关话题，请前往 Honoka Café 交流，群号：651672723。\n大水怪将会收到我们赠送的禁言大礼包。'
    ygg_server_jvm = '请在启动脚本中加入参数 -Dauthlibinjector.debug=all，然后将 logs/latest.log 上传至群文件'
    domain = '我们推测您可能使用百度搜索 LittleSkin 并使用了在中国大陆过时的 littleskin.cn，我们建议您：\n1.将域名替换成 littlesk.in；\n2.使用除百度外的搜索引擎。'
    view_hash_length_error = 'Hash 长度有误'
    view_not_200_error = '找不到材质？'
    view_no_hash_error = '请提供材质 Hash'
    mail = '请发送邮件至 support@littlesk.in，并在邮件中详细说明你的情况\n更多：https://manual.littlesk.in/email.html'
    csl_log = 'CustomSkinLoader 的日志通常位于 .minecraft/CustomSkinLoader/CustomSkinLoader.log，请将文件直接发送至群内。'
    csl_config_littleskin = '请参照「手动修改配置文件」\nhttps://manual.littlesk.in/newbee/mod.html#%E6%89%8B%E5%8A%A8%E4%BF%AE%E6%94%B9%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6'
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
    join_welcome = '欢迎加入 LittleSkin 官方用户交流群！\n提问前请先仔细阅读群内置顶公告，若直接提问可能不会被回答或被禁言。'
    pay_for_help = '在群里和大佬吹牛逼帮助不了你的问题？\nhttps://afdian.net/@tnqzh123 \n购买一对一帮助服务即可快速解决你的问题！'
    question_keywords: List[str] = ['为什么', '怎么回事', '为啥', '问个问题', '请问', '问一下', '如何解决',
                                    '我想问', '什么问题', '咋回事', '怎么办', '怎么解决']
    log_minecraft = '请使用启动器的「测试游戏」功能启动游戏，并在复现问题后导出日志发送至群内。如果问题与外置登录有关，请在启动器的「 JVM 参数」设置中填入 -Dauthlibinjector.debug'
    log_launcher = '请在启动器中复现你的问题，然后导出启动器日志发送至群内'
    java_latest = '''请更新到最新的 Java 版本，将下面链接复制到浏览器中下载
Windows x64: 
   Java 8 - https://download.bell-sw.com/java/8u322+6/bellsoft-jre8u322+6-windows-amd64-full.msi
   Java 17 - https://download.bell-sw.com/java/17.0.2+9/bellsoft-jre17.0.2+9-windows-amd64-full.msi

Windows x32:
   Java 8 - https://download.bell-sw.com/java/8u322+6/bellsoft-jre8u322+6-windows-i586-full.msi
   Java 17 - https://download.bell-sw.com/java/17.0.2+9/bellsoft-jre17.0.2+9-windows-i586-full.msi

macOS(Intel): 
   Java 8 - https://download.bell-sw.com/java/8u322+6/bellsoft-jre8u322+6-macos-amd64-full.pkg
   Java 17 - https://download.bell-sw.com/java/17.0.2+9/bellsoft-jre17.0.2+9-macos-amd64-full.pkg

macOS(M1)
   Java 8 - https://download.bell-sw.com/java/8u322+6/bellsoft-jre8u322+6-macos-aarch64-full.pkg
   Java 17 - https://download.bell-sw.com/java/17.0.2+9/bellsoft-jre17.0.2+9-macos-aarch64-full.pkg'''
    hmcl_latest = '''请到 HMCL 官网下载最新版本的 HMCL 启动器
http://ci.huangyuhui.net/job/HMCL-stable/lastSuccessfulBuild/artifact/HMCL/build/libs/HMCL-3.5.3.jar'''
