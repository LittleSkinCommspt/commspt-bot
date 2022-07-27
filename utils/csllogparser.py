from typing import Dict, List, Set, Optional, Tuple
import re
import json


class cslLogParser(object):
    log_raw: str
    log_splited: List[str]
    #

    def __init__(self, cslLogRaw: str):
        self.log_raw = cslLogRaw
        self.log_splited = cslLogRaw.split('\n')

    @staticmethod
    def _getItem(pattern, string, group) -> Optional[str]:
        _r = re.search(pattern, string)
        if _r:
            return _r.group(group)
        else:
            return None

    @staticmethod
    def _getAllItem(pattern, string, group) -> set:
        _s = set()
        _r = re.finditer(pattern, string)
        for _i in _r:
            _s.add(_i.group(group))
        return _s

    @property
    def cslVersion(self) -> str:
        '''获取 CSL 版本号'''
        return self._getItem(r'CustomSkinLoader (.*)', self.log_splited[0], 1).strip()

    @property
    def mcVersion(self) -> Optional[str]:
        '''获取 MC 版本号'''
        return self._getItem(r'Minecraft: (.*)\(.*\)', self.log_raw, 1)

    @property
    def playersList(self) -> set:
        '''获取 玩家列表'''
        return self._getAllItem(r'Loading (.*)\'s profile', self.log_raw, 1)

    @property
    def firstPlayer(self) -> str:
        return self._getItem(r'Loading (.*)\'s profile', self.log_raw, 1)

    @property
    def responseContents(self) -> List[str]:
        '''获取 API 响应（JSON 格式）'''
        return [json.loads(_i) for _i in self._getAllItem(r'Content: ({.*})', self.log_raw, 1)]

    @property
    def loadFrom(self) -> Dict[Optional[str], Optional[str]]:
        _d = dict()
        for p in self.playersList:
            isProfileLoaded = re.search(
                rf'{p}\'s profile loaded.', self.log_raw)
            if isProfileLoaded:
                # profileLoadedStartLoc, _ = isProfileLoaded.span()
                # print(profileLoadedStartLoc)
                trytoLoad = re.finditer(
                    rf'\[.*\] \[{p}.* INFO\] .* Try to load profile from \'(.*)\'\.', self.log_raw)
                apis: List[str] = list()
                for t in trytoLoad:
                    apiName = t.group(1)
                    apis.append(apiName)
                _d[p] = apis[-1]
            else:
                _d[p] = None
        return _d

    @property
    def exceptionLines(self) -> List[str]:
        '''获取 异常信息'''
        _l = list()
        for _i in self.log_splited:
            if '(Exception:' in _i:
                _l.append(_i.strip())
        return _l

    @property
    def javaVersion(self) -> Optional[str]:
        '''获取 Java 详细版本'''
        return self._getItem(r'Java Version: (.*)', self.log_raw, 1)


def cslHandler(log_raw: str, fromLittleSkin: bool = True) -> Tuple[str, str, str, str]:
    C = cslLogParser(log_raw)
    # 
    envMessage = f'''=== 环境信息 ===
CSL {C.cslVersion} | MC {C.mcVersion} | Java {C.javaVersion}'''
    # 
    firstPlayer = C.firstPlayer
    fromApi = C.loadFrom[firstPlayer]
    playerInfoMessage = f'''=== 主玩家信息 ===
{firstPlayer} (from {fromApi})'''
    # 
    exceptionLines = list()
    for i in C.exceptionLines:
        if firstPlayer in i:
            exceptionLines.append(i)
    
    # 
    diaMessages: List[str] = list()
    if not C.javaVersion:
        diaMessages.append('[WARN] 过时的 CSL 版本，请更新你的 CSL')
    for rc in C.responseContents:
        if 'skins' in rc and 'slim' in rc['skins'] and C.mcVersion == '1.7.10':
            diaMessages.append('[ERROR] 试图在 1.7.10 中加载 Slim 模型的皮肤')
            break
    for l in exceptionLines:
        if 'timed out' in l:
            diaMessages.append('[ERROR] 请求材质时连接超时，请检查网络是否正常')
            break
    for l in exceptionLines:
        if 'SSLException' in l:
            diaMessages.append('[ERROR] SSL 验证错误')
            break
    for l in exceptionLines:
        if 'Connection reset' in l:
            diaMessages.append('[ERROR] 请求材质时连接重置，请检查网络是否正常')
            break
    # 
    if not exceptionLines:
        exceptionLines.append('[INFO] 默认角色没有异常')
    exceptionMessage = '\n'.join(exceptionLines)
    if not diaMessages: # 没有检测到典型错误
        diaMessages.append('[TIPS] 未能与任何一个典型错误匹配')
    diaMessage = '\n'.join(diaMessages)
    # 
    return envMessage, playerInfoMessage, exceptionMessage, diaMessage
