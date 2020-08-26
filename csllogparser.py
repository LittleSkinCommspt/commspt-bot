from typing import Dict, List, Set, Optional, Tuple
from texts import TextFields as tF
import re
import json
import requests


class cslLogParser(object):
    log_raw: str
    log_splited: List[str]
    #
    cslVersion: str
    mcVersion: Optional[str]
    javaVersion: Optional[str]
    javaSubVersion: Optional[int]
    isLsOldDomain: bool
    players: Set[str]
    loadFrom: Dict[Optional[str], Optional[str]]
    responseContents: List[dict]

    def __init__(self, cslLogRaw: str):
        self.log_raw = cslLogRaw
        self.log_splited = cslLogRaw.split('\n')
        self.cslVersion = self._getCslVersion()
        self.mcVersion = self._getMcVersion()
        self.javaVersion = self._getJavaVersion()
        self.javaSubVersion = self._getJavaSubVersion()
        self.isLsOldDomain = self._isLsOldDomain()
        self.players = self._getPlayersList()
        self.loadFrom = self._getLoadFrom()
        self.responseContents = self._getResponseContents()

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

    def _getCslVersion(self) -> str:
        '''获取 CSL 版本号'''
        return self._getItem(r'CustomSkinLoader (.*)', self.log_splited[0], 1)

    def _getMcVersion(self) -> Optional[str]:
        '''获取 MC 版本号'''
        return self._getItem(r'Minecraft: (.*)\(.*\)', self.log_raw, 1)

    def _isLsOldDomain(self) -> bool:
        '''是否为 LittleSkin 旧域名'''
        return 'littleskin.cn/' in self.log_raw

    def _getPlayersList(self) -> set:
        '''获取 玩家列表'''
        return self._getAllItem(r'Loading (.*)\'s profile', self.log_raw, 1)

    def _getResponseContents(self) -> List[str]:
        '''获取 API 响应'''
        return [json.loads(_i) for _i in self._getAllItem(r'Content: ({.*})', self.log_raw, 1)]

    def _getLoadFrom(self) -> Dict[Optional[str], Optional[str]]:
        _d = dict()
        for p in self.players:
            isProfileLoaded = re.search(
                rf'{p}\'s profile loaded.', self.log_raw)
            if isProfileLoaded:
                profileLoadedStartLoc, _ = isProfileLoaded.span()
                print(profileLoadedStartLoc)
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

    def _getJavaVersion(self) -> Optional[str]:
        '''获取 Java 详细版本'''
        return self._getItem(r'Java Version: (.*)', self.log_raw, 1)

    def _getJavaSubVersion(self) -> Optional[int]:
        '''获取 Java 小版本号（数字）'''
        if self.javaVersion:
            return int(self._getItem(r'Java Version: .*_(.*),', self.log_raw, 1))
        else:
            return None


def cslHandler(log_raw: str, fromLittleSkin: bool = True) -> Tuple[str, Set[str]]:
    C = cslLogParser(log_raw)

    _s = str()
    for p in C.players:
        fromApi = C.loadFrom[p]
        _s = f'{_s}{p} (from {fromApi})\n'

    s = _s.strip('\n')
    envMessage = f'''CSL {C.cslVersion}, MC {C.mcVersion}
Java {C.javaVersion}
##### Players #####
{s}
##### Problems #####
'''
    diaMessages: Set[str] = set()
    for rc in C.responseContents:
        if 'skins' in rc and 'slim' in rc['skins'] and C.mcVersion == '1.7.10':
            diaMessages.add('[ERROR] 试图在 1.7.10 中加载 Slim 模型的皮肤\n')
    if C.javaSubVersion and C.javaSubVersion < 111:
        diaMessages.add('[WARN] Java 版本过低，影响到使用 Let\'s Encrypt 的站点\n')
    if fromLittleSkin and C.isLsOldDomain:
        diaMessages.add(f'[WARN] {tF.domain}\n')
    if diaMessages == set():
        diaMessages.add('[TIPS] 未能与任何一个典型错误匹配，请人工检查日志\n')
    return envMessage, diaMessages


def aoscPastebin(url: str, fromLittleSkin: bool = True) -> str:
    rawUrl = f'{url}/raw'
    r = requests.get(rawUrl)
    m1, m2 = cslHandler(r.text, fromLittleSkin=fromLittleSkin)
    m3 = str().join(m2)
    return f'{m1}{m3}'.strip('\n')
