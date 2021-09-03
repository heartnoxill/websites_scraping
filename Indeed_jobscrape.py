import requests
from bs4 import BeautifulSoup
import pandas as pd

# Remote Programmer Jobs in United States
def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84'}
    url = f"https://www.indeed.com/jobs?q=programmer&l=Remote&start={page}"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'slider_container')
    for item in divs:
        title = item.find('span').text.strip()
        if title == 'new':
            buffer = item.find_next('span')
            title = buffer.find_next('span').text.strip()
        company = item.find('span', class_ ="companyName").text.strip()
        try:
            salary = item.find('span', class_ ="salary-snippet").text.strip()
        except:
            salary = ''
        summary = item.find('div', {'class': 'job-snippet'}).text.strip().replace('\n','')
        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)

joblist = []
# c = extract(0)
# print(transform(c))
# print(joblist)

for i in range(0, 50):
    print(f'Getting page {i} ')
    c = extract(i)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs_indeed.csv')