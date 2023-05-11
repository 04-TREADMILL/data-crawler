import os

import openai

openai.api_key = os.getenv('OPENAI_API_KEY')


class Chat:
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model

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
    with open(filepath, newline='') as inf, open(os.path.join(dirname, f"mark.{filename}"), 'w', newline='') as outf:
        for line in inf:
            buf += line
            if len(buf) > 3072:
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
```{text}
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
"""
    chat = Chat()
    return chat.chat(prompt=prompt)


main("issues/tmp/microsoft.vscode.comments.1.csv")