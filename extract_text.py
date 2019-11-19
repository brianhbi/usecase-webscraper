'''
Contains functions that scrape the html pages.
'''
from bs4 import BeautifulSoup
import requests
import re

# Input: url link
# Output: scraped and cleaned text
def scrape_text(link):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}  # Request will appear like it's coming from Chrome browser
    try:
        url = requests.get(link, allow_redirects=False, headers=headers, timeout=10)
        soup = BeautifulSoup(url.content, 'html.parser')
        text = soup.find_all(text=True)

        output = ''
        tags = ['p', 'b', 'i', 'em']

        for t in text:
            if t.parent.name in tags:  # maybe add 'and len(t) is greater than 200'
                output += '{} '.format(t)

        clean_output = clean_text(output)
        # print("Link successfully scraped!")
        return clean_output

    except Exception as x:
        # print('Failed to scrape link :(')
        return ""

# Input: text
# Output: cleaned text (lowercase, )
def clean_text(text):
    text = re.sub('[^A-Za-z0-9 ,./:;?]+', '', text)
    clean_text = " ".join(text.split())  # remove duplicate whitespaces and newline characters
    return clean_text.lower()
