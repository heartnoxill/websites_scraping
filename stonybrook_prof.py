import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

global prof_url
global buffer
global result
global infolist

buffer = []
prof_url = []
result = []
infolist = []

def extract():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'}
    url = f"https://www.cs.stonybrook.edu/people/faculty"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def extract_prof(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'}
    url = f"https://www.cs.stonybrook.edu{page}"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    global result
    for a in soup.find_all('a', href=True):
        buffer.append(a['href'])
        result = [i for i in buffer if i.startswith('/people/faculty/')]
        result = list(set(result))
        # print(result)
    return result

def transform_prof(soup):
    divs = soup.find_all('div', class_= "content")
    # print(len(divs))
    for item in divs:
        name = item.find('h1')
        name = cleanhtml(str(name))
        # print(name)
        pos = item.find('div', {'class':'field field-name-field-jobtitle field-type-text field-label-hidden'})
        pos = cleanhtml(str(pos))
        # print(pos)
        email = item.find('div', {'class':'field field-name-field-protected-email field-type-email field-label-inline clearfix'})
        email = cleanhtml(str(email))
        # print(email)
        web = item.find('div', {'class':'field field-name-field-facultywebsite field-type-link-field field-label-inline clearfix'})
        web = cleanhtml(str(web))
        # print(web)
        foi = item.find('div',{'class': "field field-name-field-interests field-type-text-long field-label-hidden"})
        foi = cleanhtml(str(foi))
        # print(foi)
        res = item.find('div', {'class': "field field-name-field-research field-type-text-long field-label-hidden"})
        res = cleanhtml(str(res))
        # print(res)

        info = {
            'name': name,
            'position': pos,
            'email': email,
            'website': web,
            'field of interest': foi,
            'research': res
        }
        infolist.append(info)

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def main():
    global result
    global infolist
    print("Working in progress...")
    c = extract()
    transform(c)
    # print(prof_url)
    for profpage in result:
        # print(profpage)
        d = extract_prof(profpage)
        transform_prof(d)
    # print(infolist.head())
    df = pd.DataFrame(infolist)
    # print(df.head())
    df.to_csv('prof_stonybrook.csv')
    print("Done!")

if __name__ == '__main__':
    main()
