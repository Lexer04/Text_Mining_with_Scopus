import csv
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

filejson = "reinforcement.json"
count = 0
count2 = 0
count3 = 0
def open_json(file):
    df = pd.read_json(file)
    return df
def get_abstractdc(link):
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"}
    url_abstract = ('' + link)
    r = requests.get(url=url_abstract, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    title = soup.find('h2', attrs={'class': "h3"})
    author = [item.text for item in soup.find_all('span', attrs={'class': 'previewTxt'})]
    abstract = soup.find('section', attrs={'id': 'abstractSection'}).find("p").text
    keyword = [item.text for item in soup.find_all('span', attrs={'class': 'badges'})]
    print(title.text)
    #===============================================
    # Write the data to the CSV file
    scopus = {
        'Title': title.text if title else '',
        'Author': ','.join(author),
        'Date' : date,
        'Abstract': abstract,
        'Keyword': ','.join(keyword),
        'URL': url_abstract
    }
    json_object = json.dumps(scopus, indent=4)
    outfile.write(json_object)
    #===============================================
if __name__ == '__main__':
    with open("ReiforcementLearning.json", "w", newline='') as outfile:
        dfscopus = open_json(filejson)
        end = len(dfscopus)
        print(end)
        data = dfscopus.loc[count]["search-results"]["entry"][count2]["link"][2]['@href']
        print(data)
        while count < end:
            while count2 < 25:
                link = dfscopus.loc[count]["search-results"]["entry"][count2]["link"][2]['@href']
                date = dfscopus.loc[count]["search-results"]["entry"][count2]["prism:coverDisplayDate"]
                print(link)
                count2 = count2 + 1
                count3 = count3 + 1
                print('{}/{}'.format(count3,end))
                if not link:
                    break  # Exit the loop when there are no more URLs to process
                get_abstractdc(link)
                if count2 == 25:
                    count = count + 25
                    count2 = 0
                    # end = end - 25
                if end == count3:
                    print("Data has been written to json file")
                    break
