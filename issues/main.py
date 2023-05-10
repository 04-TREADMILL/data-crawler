import csv
import json
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import requests

OWNER = "microsoft"
REPO = "vscode"
PAGES = 1
PER_PAGE = 100
limited = False

fieldnames = ['id', 'text']


# 定义一个下载 issue 数据的函数
def download_issues(owner, repo, page):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/issues?state=open&per_page={PER_PAGE}&page={page + 1}",
        headers=headers)
    if response.status_code != requests.codes.ok:
        global limited
        limited = True
        print("rate limit")
        return
    raw = response.content.decode()
    issues = json.loads(raw)
    issues = [{"id": PER_PAGE * page + idx, "text": issue["title"]}
              for idx, issue in enumerate(issues)
              if len(issue["title"]) > 32]
    with open(f"{owner}.{repo}.{page}.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        writer.writerows(issues)
    time.sleep(random.randint(3, 7))


# 定义一个任务队列
task_queue = Queue()

# 将所有任务添加到队列中
for i in range(PAGES):
    task_queue.put(i)

# 创建线程池
with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    # 不断地从任务队列中取出任务并执行
    while not task_queue.empty() and not limited:
        i = task_queue.get()
        executor.submit(download_issues, OWNER, REPO, i)
        task_queue.task_done()

print("DONE")
