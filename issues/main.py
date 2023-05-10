import csv
import json
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from queue import Queue

import requests


class DataType(Enum):
    ISSUE_TITLE = 1,
    ISSUE_COMMENT = 2


OWNER = "microsoft"
REPO = "vscode"
PAGE_ST = 46
PAGE_ED = 46
PER_PAGE = 100
TYPE = DataType.ISSUE_COMMENT


def clean(text: str) -> str:
    return text.strip().replace('\n', ' ')


def get_proxy():
    return requests.get("http://demo.spiderpy.cn/get/").json()


# 下载函数
def downloader(owner, repo, page):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    params = {
        "sort": "created",
        "direction": "asc",
        "per_page": PER_PAGE,
        "page": page
    }

    if TYPE == DataType.ISSUE_TITLE:
        params.setdefault("state", "all")
        url = "issues"
        dict_key = "title"
        filename = f"{owner}.{repo}.issues.{page}.csv"
    elif TYPE == DataType.ISSUE_COMMENT:
        url = "issues/comments"
        filename = f"{owner}.{repo}.comments.{page}.csv"
        dict_key = "body"
    else:
        raise RuntimeError("unsupported type")

    proxy = get_proxy().get("proxy")
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/{url}", params=params, headers=headers,
        proxies={"http": "http://{}".format(proxy)})
    if response.status_code != requests.codes.ok:
        print("rate limit")
        raise RuntimeError("rate limit")

    raw = response.content.decode()
    issues = json.loads(raw)
    issues = [{"id": (page - 1) * PER_PAGE + idx + 1, "text": clean(issue[dict_key])} for idx, issue in
              enumerate(issues)]

    fieldnames = ['id', 'text']
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
        # writer.writeheader()
        writer.writerows(issues)

    print(page)
    time.sleep(random.randint(3, 7))


# 任务队列
task_queue = Queue()

# 将所有任务添加到队列中
for i in range(PAGE_ST, PAGE_ED + 1):
    task_queue.put(i)

# 创建线程池
with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    # 不断地从任务队列中取出任务并执行
    while not task_queue.empty():
        i = task_queue.get()
        executor.submit(downloader, OWNER, REPO, i)
        task_queue.task_done()

print("ALL DONE")
