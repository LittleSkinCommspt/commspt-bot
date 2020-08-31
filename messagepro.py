import re
from typing import List, Optional, Tuple

from graia.application.entry import (At, Group, GroupMessage, MessageChain,
                                     Plain, Quote, Source)
from graia.broadcast.exceptions import ExecutionStop

import settings
from permissionshandler import PermissionsHandler


# 一些消息过滤器
def exceptGroups(group_list: List[int]):
    '''在指定群聊内禁用'''
    def wrapper(group: Group):
        if group.id in group_list:
            raise ExecutionStop()
    return wrapper


def inGroups(group_list: List[int]):
    '''仅在指定群聊内启用'''
    def wrapper(group: Group):
        if not group.id in group_list:
            raise ExecutionStop()
    return wrapper


def adminOnly(gm: GroupMessage):
    '''仅管理员'''
    M = MessagePro(gm, settings.commandSymbol)
    P = PermissionsHandler(M.sender_id)
    if not P.isAdmin():
        raise ExecutionStop()

def onCommand(command_name: str):
    '''在特定指令时执行

    Args:
        command_name: 指令名称（不带标识符）'''
    def wrapper(gm: GroupMessage):
        M = MessagePro(gm, settings.commandSymbol)
        P = PermissionsHandler(M.sender_id)
        if P.isBlocked():
            raise ExecutionStop()
        if not M.plain_message:
            raise ExecutionStop()
        if M.Command.cmd != command_name:
            raise ExecutionStop()
    return wrapper

def onWord(word: str):
    '''在消息中有特定文字时执行

    Args:
        word: 文字'''
    def wrapper(gm: GroupMessage):
        M = MessagePro(gm, settings.commandSymbol)
        P = PermissionsHandler(M.sender_id)
        if P.isBlocked():
            raise ExecutionStop()
        if not M.plain_message:
            raise ExecutionStop()
        if not word in M.plain_message:
            raise ExecutionStop()
    return wrapper


def onWords(words_list: List[str]):
    '''在消息中有特定文字时执行

    Args:
        words_list: 关键字列表'''
    def wrapper(gm: GroupMessage):
        M = MessagePro(gm, settings.commandSymbol)
        P = PermissionsHandler(M.sender_id)
        if P.isBlocked():
            raise ExecutionStop()
        inList = False
        if not M.plain_message:
            raise ExecutionStop()
        for word in words_list:
          if word in M.plain_message:
              inList = True
              break
        if not inList:
          raise ExecutionStop()
    return wrapper

def onMatch(pattern: str):
    '''在消息匹配正则表达式时执行

    Args:
        pattern: 正则表达式（必须为 str）'''
    def wrapper(gm: GroupMessage):
        M = MessagePro(gm, settings.commandSymbol)
        P = PermissionsHandler(M.sender_id)
        if P.isBlocked():
            raise ExecutionStop()
        if not M.plain_message:
            raise ExecutionStop()
        if not re.match(pattern, M.plain_message):
            raise ExecutionStop()
    return wrapper
    

class MessagePro(object):
    '''指令解析器'''
    _commandSymbol: str
    messagechain: MessageChain
    sender_id: int
    plain_message: Optional[str]
    quote_plain_message: str
    source: Optional[Source]
    at: List[At]
    permission: PermissionsHandler

    class Command(object):
        '''指令

        `cmd` 为指令，`args` 为参数'''
        cmd: Optional[str]
        args: Optional[str]
        argsList: Optional[List[str]]

    def __init__(self, _groupmessage: GroupMessage, _command_symbol: str = settings.commandSymbol) -> None:
        '''初始化指令解析器

        Args:
            _groupmessage: `GroupMessage` 对象
            _command_symbol: 指令标识符'''
        self._commandSymbol = _command_symbol
        self.messagechain = _groupmessage.messageChain
        self.sender_id = _groupmessage.sender.id
        self.plain_message = self._getPlainMessage(self.messagechain)
        self.at = self._getAt()
        self.Command.cmd, self.Command.args, self.Command.argsList = self._getCommand()
        self.quote_plain_message = self._getQuotePlainMessage()
        self.source = self._getSource()
        self.permission = PermissionsHandler(self.sender_id)

    def _getPlainMessage(self, _messagechain: MessageChain) -> Optional[str]:
        if _messagechain.has(Plain):
            _text = str()
            for _i in _messagechain[Plain]:
                i_text: str = _i.text
                if i_text.strip() != '':
                    _text = f'{_text} {i_text}'
            return _text.strip()
        else:
            return None

    def _getAt(self) -> List[At]:
        return self.messagechain.get(At)

    def _getQuotePlainMessage(self) -> Optional[str]:
        if self.messagechain.has(Quote):
            _quote_message: Quote = self.messagechain.get(Quote)[0]
            _origin_messagechain: MessageChain = _quote_message.origin
            _plain_message = self._getPlainMessage(_origin_messagechain)
            return _plain_message
        else:
            return None
    
    def _getSource(self) -> Optional[Source]:
            return self.messagechain[Source][0]

    def isConstance(self) -> bool:
        '''判断此 `GroupMessage` 是否为 Constance 发出'''
        return self.sender_id == settings.specialqq.constance

    def _getCommand(self) -> Tuple[Optional[str], Optional[str]]:
        if not self.plain_message:
            return None, None, None
        if self._commandSymbol in self.plain_message:
            _message_body: str = self.plain_message.split(
                '：', 1)[1] if self.isConstance() else self.plain_message
            _splited_message: list = _message_body.split(' ', 1)
            _command: str = _splited_message[0]
            _args: Optional[str] = _splited_message[1] if len(
                _splited_message) > 1 else None
            _argsList: Optional[List[str]] = _args.split() if _args else None
            cmd: str = _command.replace(
                self._commandSymbol, '')  # 只留下命令主体而不考虑命令标识符
            return cmd, _args, _argsList
        else:
            return None, None, None
