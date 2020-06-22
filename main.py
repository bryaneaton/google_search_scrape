#!/usr/bin/env python3
import pickle
import requests
import json
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"


def build_query(term):
    query = term.replace(' ', '+')
    return f"https://google.com/search?q={query}"


def response(query):
    results = []
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(build_query(query), headers=headers)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {
                    "title": title,
                    "link": link
                }
                results.append(item)
                logging.info(f'Appended {item} to result list for search: {query}')
    return json.dumps(results)

def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    data = dict()  # JSON object
    keys = range(100, 999)
    n = 0
    for i in keys:
        logging.info(f'Search term: {i}')
        data[i] = response(f'{i} new cases')
    save_obj(data, 'google_results.txt')



