import requests
import csv
from concurrent.futures import ThreadPoolExecutor
import threading

url = "https://api.stackexchange.com/2.3/questions"

params = {
    "site": "stackoverflow",
    "pagesize": 100,
    "key": "OcugRWcRkGc4BmksZoNdag(("
}

total_items = 25000  # 总计保存的数据条数
items_per_page = params['pagesize']
pages = (total_items // items_per_page) + 1  # 计算需要的页数

# 创建CSV文件并写入数据
with open('stackoverflow_data.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file, delimiter='|')

    # 写入标题行
    writer.writerow(['编号', '文本'])

    # 创建线程局部变量
    count_local = threading.local()
    count_local.count = 1


    def process_item(item):
        count = getattr(count_local, 'count', 1)

        question_id = item['question_id']
        question_text = str(item['title']).strip().replace('\n', ' ')
        writer.writerow([count, question_text])  # 写入问题的行
        count_local.count = count + 1

        if 'answers' in item:
            answers = item['answers']
            for answer in answers:
                answer_id = answer['answer_id']
                answer_text = str(answer['body']).strip().replace('\n', ' ')
                writer.writerow([count_local.count, answer_text])  # 写入回答的行
                count_local.count += 1


    def fetch_data(page):
        params['page'] = page
        response = requests.get(url, params=params)

        try:
            response.raise_for_status()
            data = response.json()
            if 'items' in data:
                return data['items']
        except (requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError) as e:
            print(f"Error fetching data from page {page}: {str(e)}")

        return []


    # 创建线程池并发起请求
    with ThreadPoolExecutor() as executor:
        # 构建任务列表
        tasks = [executor.submit(fetch_data, page) for page in range(1, pages + 1)]

        # 处理任务结果
        for task in tasks:
            items = task.result()
            for item in items:
                process_item(item)

    print('数据已保存到本地CSV文件。')
