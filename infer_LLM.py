import openai
import os
from tqdm import tqdm
import time
import re

openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")

def infer_llm(engine, instruction, exemplars, query, answer_num=5, max_tokens=2048):
    """
    Args:
        instruction: str
        exemplars: list of dict {"query": str, "answer": str}
        query: str
    Returns:
        answers: list of str
    """

    messages = [{"role": "system", "content": "You are a helpful AI assistant.."},
                {"role": "user", "content": instruction},
                {"role": "assistant", "content": "OK, I'm ready to help."},
        ]
    
    if exemplars is not None:
        for i, exemplar in enumerate(exemplars):
            messages.append({"role": "user", "content": exemplar['query']})
            messages.append({"role": "assistant", "content": exemplar['answer']})
    
    messages.append({"role": "user", "content": query})

    # engine in ["gpt-35-turbo", "gpt-4"]
    retry_times = 0
    while True:
        if retry_times > 5:
            return [""]
        time.sleep(1)
        try:
            answers = openai.ChatCompletion.create(
                engine=engine,
                messages=messages,
                temperature=0.1,
                max_tokens=max_tokens,
                top_p=0.95,
                n=answer_num,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
            )
            return [response["message"]["content"] for response in answers["choices"]]
        except Exception as e:
            print(e)
            try:
                sleep_time = re.findall(r'Please retry after (\d+) seconds.', e.user_message)
                time.sleep(int(sleep_time[0]))
            except Exception:
                if "This model's maximum context length is 32768 tokens." in e.user_message:
                    messages[-1]["content"] = messages[-1]["content"][:len(messages[-1]["content"])//2]
                    while messages[-1]["content"][-1] != ".":
                        messages[-1]["content"] = messages[-1]["content"][:-1]
                time.sleep(10)
            retry_times += 1


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))