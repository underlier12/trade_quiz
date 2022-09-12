from PyPDF2 import PdfFileReader

import PyPDF2
import re

FIRST_LINE = 'Commentary on eUCP Version 2.0 and eURC Version 1.0'
ARTICLE = 'ARTICLE'

def read_pdf(PATH: str) -> PdfFileReader:
    pdf_object = open(PATH, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_object)
    return pdf_reader

def get_text(pdf_reader: PdfFileReader, page: int) -> str:
    page_object = pdf_reader.getPage(page)
    text = page_object.extractText()
    return text

def remove_first_line(text: str, page: int) -> str:
    if page >= 100:
        margin = 6
    if page < 100:
        margin = 5
    return text[margin+len(FIRST_LINE):]

def find_article_start_positions(text: str) -> list:
    position_first = [0]
    positions = [m.start() for m in re.finditer(ARTICLE, text)]
    position_last = [len(text)]
    return position_first + positions + position_last

def divide_text(text: str, start_positions: list) -> list:
    article_candidates = []
    for idx in range(len(start_positions)-1):
        sub_text = text[start_positions[idx]:start_positions[idx+1]]
        article_candidates.append(sub_text)
    return article_candidates

def check_full_article(article: str) -> dict:
    title = None
    
def main():
    PATH = 'source/icc-commentary-on-eucp-2-0-and-eurc-1-0-article-by-article-analysis.pdf'
    pdf_reader = read_pdf(PATH)

    last_article = None
    for i in range(19, 116):
        text = get_text(pdf_reader, i)

        if i == 112:
            text = remove_first_line(text, i)
            print(text)
            start_positions = find_article_start_positions(text)
            divide_text(text, start_positions)

if __name__ == '__main__':
    main()