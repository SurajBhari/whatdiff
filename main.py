from bs4 import BeautifulSoup
import string
from json import load, loads, dump, dumps   
from os import _exit, listdir, mkdir, path
import requests
import difflib

def string_diff(str1, str2):
    differ = difflib.Differ()
    diff = list(differ.compare(str1.splitlines(), str2.splitlines()))
    return '\n'.join(diff)

try:
    config = load(open('config.json', 'r'))
except FileNotFoundError:
    print('config.json not found, please create one.')
    _exit(1)

if "data" not in listdir():
    mkdir("data")

r_chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
def rasterize_url(url):
    s = ""
    for char in url:
        if char in r_chars:
            s += char
    return s

for elem in config:
    url = elem['url']
    r_url = rasterize_url(url)
    selector = elem['selector']
    data = requests.get(url)
    if r_url not in listdir(path.join('data')):
        with open(path.join('data', r_url), 'w') as f:
            f.write(data.text)
        print(f"First iteration for {url} done.")
        continue
    with open(path.join('data', r_url), 'r') as f:
        old_data = f.read()

    """
    if old_data == data.text:
        print(f"{url} hasn't changed.")
        continue
    """
    print(f"{url} has changed.")
    soup = BeautifulSoup(data.text, 'html.parser')
    elements = soup.find_all(attrs={selector['type']:selector['value']}) 
    if not elements:
        print(f"Selector {selector['value']} not found in {url}.")
        continue
    print(elements)
    if selector['type'] == "id":
        element = elements[0]
    else:
        element = elements[selector['count']]
    
    soup = BeautifulSoup(old_data, 'html.parser')
    elements = soup.find_all(attrs={selector['type']:selector['value']}) 
    if not elements:
        print(f"Selector {selector['value']} not found in {url}.")
        continue
    if selector['type'] == "id":
        old_element = elements[0]
    else:
        old_element = elements[selector['count']]
    
    if str(element) != str(old_element):
        print(f"{url} has changed.")
        difference = string_diff(str(element), str(old_element))
        print(difference)

    with open(path.join('data', r_url), 'w') as f:
        f.write(data.text)