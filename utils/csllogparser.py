from logging import exception
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


def cslHandler(log_raw: str, fromLittleSkin: bool = True) -> Tuple[str, str, str, Set[str]]:
    C = cslLogParser(log_raw)
    # 
    envMessage = f'''=== 环境信息 ===
CSL {C.cslVersion} | MC {C.mcVersion} | Java {C.javaVersion}'''
    # 
    _s = list()
    for player in C.playersList:
        fromApi = C.loadFrom[player]
        _s.append(f'{player} (from {fromApi})')
    s = '\n'.join(_s)
    playerInfoMessage = f'''=== 玩家信息 ===
{s}'''
    # 
    exceptions = '\n'.join(C.exceptionLines)
    # 
    diaMessages: Set[str] = set()
    if not C.javaVersion:
        diaMessages.add('[WARN] 过旧的 CSL 版本，请更新你的 CSL')
    for rc in C.responseContents:
        if 'skins' in rc and 'slim' in rc['skins'] and C.mcVersion == '1.7.10':
            diaMessages.add('[ERROR] 试图在 1.7.10 中加载 Slim 模型的皮肤\n')
            break
    if 'timed out' in C.exceptionLines:
        diaMessages.add('[WARN] 疑似请求皮肤时超时，请检查网络是否正常\n')
    if 'SSL' in C.exceptionLines:
        diaMessages.add('[ERROR] SSL 验证错误')
    # if fromLittleSkin aNone and isLsOldDomain:
    #     diaMessgaes.add(f
    # if C.SSLHandShakeError
    # .   diaMessages.add(f'[ERROR] 使用过老的 Javages\n ')dd(f'[WARN] {tF.domain}\n')    
    if not diaMessages:
        diaMessages.add('[TIPS] 未能与任何一个典型错误匹配，请人工检查日志\n')
    return envMessage, playerInfoMessage, exceptions, diaMessages

