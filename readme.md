# ArXiv-Summary

## Description

A large number of papers are submitted to arXiv every day, but there are very few that are truly innovative. This tool can help retrieve the papers from arXiv daily and use GPT-4 to generate summaries for each paper. **(Even though it's possible to directly crawl the abstracts from arXiv, I just want to use GPT-4, hahaha)**

## Usage
The codes for crawling papers from arXiv are adopted from [arxiv-sanity-preserver](https://github.com/karpathy/arxiv-sanity-preserver).

Run `fetch_papers.py` to query arxiv API and create a file `db.p` that contains all information for each paper. This script is where you would modify the query, indicating which parts of arxiv you'd like to use. Note that if you're trying to pull too many papers arxiv will start to rate limit you. You may have to run the script multiple times, and I recommend using the arg `--start-index` to restart where you left off when you were last interrupted by arxiv. Use `--month` and `--date` to specify the month and date of the papers you want to retrieve. Note that I exclude the CV related papers by default as I'm not interested in. 

Run `download_pdf.py` which iterates over all papers in parsed pickle and downloads the papers into folder `pdf`.

Run `parse_pdf_to_text.py` to export all text from pdfs to files in `txt`. Make sure `pdftotext` is installed.

Run `summarize_papers.py` to generate summaries for each paper with `gpt-4-32k`. The summaries are stored in `data/sum`. I use Azure OpenAI service to do so. You can modify the `infer_LLM.py` to use your own service.
