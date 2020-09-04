import asyncio
import traceback
from io import StringIO
from typing import Callable, Dict, List, NoReturn, Optional
import os.path

import requests

from settings import github_access_token, github_listen_repos

eventIdCacheFile = 'github-event-id-cache'


class eventIdCache(object):
    filename: str

    def __init__(self, filename: str) -> NoReturn:
        self.filename = filename
        self._checkFile()

    def _checkFile(self) -> NoReturn:
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write('0')

    def writeId(self, id: str) -> NoReturn:
        with open(self.filename, 'w') as f:
            f.write(id)

    def readId(self) -> int:
        with open(self.filename, 'r') as f:
            return int(f.read())


async def polling(repo: str, req: requests.Session, Send: Callable[[str], NoReturn]):
    etag: Optional[str] = None  # ETag 可用于判断内容是否更新，也可用于判断是否为第一次轮询
    x_poll_interval: int = 60  # 默认轮询间隔为 60
    lastEvent = eventIdCache(eventIdCacheFile)
    while True:
        lastEventId = lastEvent.readId()
        if etag:
            # 使用 ETag 判断内容是否更新以节省资源
            req.headers.update({'If-None-Match': etag})
        try:
            _events = req.get(
                f'http://api.github.com.xiaojin233.cn/repos/{repo}/events?per_page=10')
            hasXPollInterval: bool = 'X-Poll-Interval' in _events.headers  # 响应头中是否包含轮询间隔
            x_poll_interval: int = int(
                _events.headers['X-Poll-Interval']) if hasXPollInterval else x_poll_interval
            if _events.status_code == 200 and etag:  # 状态码为 200 且非第一次轮询
                _j: List[Dict] = _events.json()
                lastEvent.writeId(_j[0]['id'])  # 将最新的 Event ID 写入 lastEvent
                for event in _j:
                    if int(event['id']) <= lastEventId:
                        break
                    thisType: str = event['type']
                    if thisType == 'IssuesEvent':
                        await issuesOpend(repo, event['payload'], Send)
                    elif thisType == 'PushEvent':
                        await pushEvent(repo, event, Send)
                    elif thisType == 'PullRequestEvent':
                        await pullRequestEvent(repo, event['payload'], Send)
            elif _events.status_code == 304:  # 暂时没有
                pass
            etag = _events.headers['ETag']  # 更新 ETag
        except Exception:  # 防止突然宕
            traceback.print_exc()
        await asyncio.sleep(x_poll_interval)


async def issuesOpend(repo: str, payload: dict, Send: Callable[[str], NoReturn]):
    this = payload['issue']
    action: str = payload['action']
    _number: int = this['number']
    _title: str = this['title']
    _html_url: str = this['html_url']
    if action == 'opened':
        await Send(f'[{repo}] #{_number} {_title}\n1 issue has been opened.\n{_html_url}')
    elif action == 'closed':
        await Send(f'[{repo}] #{_number} {_title}\n1 issue has been closed.\n{_html_url}')


async def pushEvent(repo: str, event: dict, Send: Callable[[str], NoReturn]):
    _operator: str = event['actor']['display_login']
    _commitsNumber = len(event['payload']['commits'])
    if _commitsNumber == 1:
        _desc = event['payload']['commits'][0]['message']
        await Send(
            f'[{repo}] {_operator} pushed {_commitsNumber} commit:\n{_desc}')
    else:
        await Send(f'[{repo}] {_operator} pushed {_commitsNumber} commits.')


async def pullRequestEvent(repo: str, payload: dict, Send: Callable[[str], NoReturn]):
    action: str = payload['action']
    this: dict = payload['pull_request']
    _number: int = this['number']
    _title: str = this['title']
    _html_url: str = this['html_url']
    _merged: bool = this['merged']
    #
    statusWord: Optional[str]
    if action == 'opened':
        statusWord = 'opened'
    elif action == 'closed':
        statusWord = 'merged' if _merged else 'closed'
    else:
        statusWord = None
    if not statusWord:
        await Send(f'[{repo}] #{_number} {_title}\n1 pull request has been {statusWord}. \n{_html_url}')

# 初始化 Session 对象
req = requests.session()
req.headers.update({'Authorization': f'token {github_access_token}'})
req.headers.update({'Accept': 'application/vnd.github.v3+json'})


def githubListener(send_func: Callable[[str], NoReturn]) -> asyncio.Task:
    coros = list()
    repos: List[str] = github_listen_repos
    for repo in repos:
        coros.append(polling(repo, req, send_func))
    loop = asyncio.get_event_loop()
    return loop.create_task(loop.run_until_complete(asyncio.wait(coros)))
