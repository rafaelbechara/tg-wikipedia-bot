import re
import requests
from lxml import etree

user_request = input('What are you looking for?\n')
formatted_request = user_request.title().replace(' ', '_')
url = 'https://en.wikipedia.org/wiki/' + formatted_request

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status() 
except requests.exceptions.RequestException as e:
    print(f"Error: Could not retrieve the page. {e}")
    exit()

tree = etree.HTML(response.content)

first_paragraph = tree.xpath('string(/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[2])')
second_paragraph = tree.xpath('string(/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[3])')

wikiresult = (f'\n{first_paragraph}\n{second_paragraph}')
wikiresult = re.sub(r'\[.*?\]', '', wikiresult)

print(wikiresult)