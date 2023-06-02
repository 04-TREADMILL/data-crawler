# data-crawler

## Reference

- https://docs.github.com/en/rest/issues/comments?apiVersion=2022-11-28#list-issue-comments-for-a-repository
- https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28#list-repository-issues
- https://github.com/jhao104/proxy_pool

## doc

### 约定的数据格式

```csv
id|text|mark
0|xxx|1
```

### 数据来源

- stackoverflow titles
- github issue titles and comments

### 数据爬取

- 利用 stackoverflow 和 github 开放的 apis 获取数据
- 利用多线程技术加速爬取速度
- 爬取结果
  - stackoverflow titles 25000 条
  - github issue titles 30000 条
  - github issue comments 30000 条

### 数据标注

分为两个步骤

1 利用文本相似度检测，排除了可能与测试集相交的数据
2. 利用 openapi gpt-3.5-turbo 模型，对爬取的数据进行初步标注
3. 使用人工众包的方案，标注了 1800 条数据，构成最终扩充的训练集