from typing import Callable, List
import asyncio

import requests
import settings
from io import StringIO


async def event_handler(repo: str, req, Send):
    etag = None
    lastEvent = StringIO()
    lastEvent.write('0')
    while True:
        lastEventId = lastEvent.getvalue()
        if etag:
            req.headers.update({'If-None-Match': etag})
        _event = req.get(
            f'http://api.github.com.xiaojin233.cn/repos/{repo}/events?per_page=10')
        # Send(_event.status_code)
        hasXPollInterval = 'X-Poll-Interval' in _event.headers
        x_poll_interval: int = int(
            _event.headers['X-Poll-Interval']) if hasXPollInterval else 60
        if _event.status_code == 200:
            _j = _event.json()
            lastEvent.truncate(0) # clear lastEvent
            lastEvent.seek(0)
            lastEvent.write(_j[0]['id']) # write the latest event id into lastEvent
            if etag:
                for i in _j:
                    if int(i['id']) <= int(lastEventId):
                        break
                    thisType = i['type']
                    if thisType == 'IssuesEvent':
                        await issuesOpend(repo, i['payload'], Send)
                    elif thisType == 'PushEvent':
                        await pushEvent(repo, i, Send)
                    elif thisType == 'PullRequestEvent':
                        await pullRequestEvent(repo, i['payload'], Send)
        etag = _event.headers['ETag']
        await asyncio.sleep(x_poll_interval)


async def issuesOpend(repo: str, payload: dict, Send):
    this = payload['issue']
    action = payload['action']
    _number = this['number']
    _title = this['title']
    _html_url = this['html_url']
    if action == 'opened':
        await Send(f'[{repo}] #{_number} {_title}\n1 issue has been opened\n{_html_url}')
    elif action == 'closed':
        await Send(f'[{repo}] #{_number} {_title}\n1 issue has been closed\n{_html_url}')


async def pushEvent(repo: str, event: dict, Send):
    _operator = event['actor']['display_login']
    _commitsNumber = len(event['payload']['commits'])
    if _commitsNumber == 1:
        _desc = event['payload']['commits'][0]['message']
        await Send(
            f'[{repo}] {_operator} pushed {_commitsNumber} commit:\n{_desc}')
    else:
        await Send(f'[{repo}] {_operator} pushed {_commitsNumber} commits.')


async def pullRequestEvent(repo: str, payload: dict, Send):
    action = payload['action']
    this = payload['pull_request']
    _number = this['number']
    _title = this['title']
    _html_url = this['html_url']
    if action == 'opened':
        await Send(f'[{repo}] #{_number} {_title}\n1 pull request has been opened\n{_html_url}')
    elif action == 'closed':
        await Send(f'[{repo}] #{_number} {_title}\n1 pull request has been closed\n{_html_url}')


req = requests.session()
req.headers.update({'Authorization': f'token {settings.github_access_token}'})
req.headers.update({'Accept': 'application/vnd.github.v3+json'})


def githubListener(send_func) -> list:
    tasks = list()
    for repo in settings.github_listen_repos:
        tasks.append(event_handler(repo, req, send_func))
    return tasks

if __name__ == "__main__":
    async def s(m):
        print(m)
    githubListener(s)
