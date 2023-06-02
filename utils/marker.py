import os
import time
from functools import wraps

import openai

openai.api_key = os.getenv('OPENAI_API_KEY')


def rate_limited(max_calls_per_minute):
    interval = 60 / max_calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed_time = time.time() - last_called[0]
            if elapsed_time < interval:
                time.sleep(interval - elapsed_time)
            last_called[0] = time.time()
            return func(*args, **kwargs)

        return wrapper

    return decorator


class Chat:
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model

    @rate_limited(3)
    def chat(self, prompt):
        messages = [{'role': 'user', 'content': prompt}]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0,  # this is the degree of randomness of the model's output
        )
        return response.choices[0].message['content']


def main(filepath: str):
    buf = ""
    dirname, filename = os.path.split(filepath)
    with open(filepath, newline='', encoding='utf-8') as inf, \
            open(os.path.join(dirname, f"mark.{filename}"), 'w', newline='', encoding='utf-8') as outf:
        for line in inf:
            buf += line
            if len(buf) > 2048:
                resp = mark(buf)
                outf.write(resp)
                buf = ""
        if len(buf) > 0:
            resp = mark(buf)
            outf.write(resp)


def mark(text: str) -> str:
    prompt = f"""
Here are messages in CSV format (pipe character as value separator) with the following keys:
index|message
Identify the emotion of each line in the software engineering text delimited by triple backticks.
```
{text}
```
Classify each line of the text as '1' or '-1' or '0':
- '1' means it expresses positive emotion
- '-1' means it expresses negative emotion
- '0' means it is neutral
Provide them in CSV format (pipe character as value separator) with the following keys:
index|message|label
Remember that:
- 'index' and 'message' is the same as the original messages.
- 'label' is the classification result.
- do not display field names.
- do not forget to display message.
"""
    print(prompt)
    chat = Chat()
    res = chat.chat(prompt=prompt)
    print(res)
    return res


for i in range(1, 11):
    main(f"microsoft.vscode.issues.{i}.csv")
