import os
import time
import datetime

from infer_LLM import infer_llm
from utils import Config

if not os.path.exists(Config.sum_dir):
    print('creating ', Config.sum_dir)
    os.makedirs(Config.sum_dir)

instruction = """I want you to act as a human reader of the paper. You need to read through the paper related to Artificial Intelligence and Machine Learning and compose a comprehensive summary. The summary should encompass the problem addressed by the paper, its main idea, the employed methodologies, and the obtained experimental results. Please aim for a summary length of approximately 300 words. Please write this summary in both Chinese and English. Should the provided paper be incomplete, kindly refrain from attempting to extend it and proceed directly to composing the summary."""

have = set(os.listdir(Config.sum_dir))
files = os.listdir(Config.txt_dir)
for i,f in enumerate(files):
    time_start = time.time()
    sum_filename = f[:-4] + '.sum.txt'
    if sum_filename in have:
        print('%d/%d skipping %s, already exists.' % (i, len(files), sum_filename, ))
        continue
    txt_filename = os.path.join(Config.txt_dir, f)
    sum_filename = os.path.join(Config.sum_dir, sum_filename)

    content = open(txt_filename, 'r').read()
    query = "Here is the paper content:\n" + content

    summary = infer_llm("gpt-4-32k", instruction, None, query, 1, 1024)[0]
    
    with open(sum_filename, 'w') as wf:
        wf.write(summary)
    
    time_end = time.time()
    td = str(datetime.timedelta(seconds=int(time_end - time_start)))
    print('%d/%d %s' % (i, len(files), td))

    time.sleep(5)