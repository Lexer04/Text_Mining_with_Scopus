import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import csv

api_key = '0369565b95c1887b9d9740df66f99ec3'
headers = {
    "X-ELS-APIKey": api_key,
}

topic_research = open('keyword.txt', 'r')
url = "https://api.elsevier.com/content/search/scopus?&count=25"

api_index=0
start_date = 2012
end_date = 2023
period = 1
count = 0
count2 = 0
total = 0
data = []
start = 0
year = 1

allfile = open ("ComputerVision{}.json".format(start_date), "w")
outfile = open ("ComputerVisionAbstract{}.json".format(start_date), "w")

# allfile = open ("ComputerVision{} to {}.json".format(start_date,year), "w") #if you want it to be period of time
# outfile = open ("ComputerVisionAbstract{} to {}.json".format(start_date,year), "w") #if you want it to be period of time

def scopus_search():
    global data,total
    # print("{} - {}".format(start_date, start_date + period))
    data = []
    query_scopus = {}
    query_scopus["query"] = keyword
    query_scopus["start"] = api_index
    query_scopus["date"] = str(start_date)
    #query_scopus["date"] = str(start_date) + "-" + str(start_date + year) ## If you want it to be a period of time
    response = requests.get(url, params=query_scopus, headers=headers)
    data = response.json()
    totalResults = data["search-results"]["opensearch:totalResults"]
    total = int(totalResults)
    print(total)

def get_abstractdc(linky):
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"}
    url_abstract = ('' + linky)
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
    topic = topic_research.readline().strip()  ## THIS NEEDS TO BE OUTSIDE OF THE LOOP
    keyword = topic  ## THIS ONE ALSO

    while True:
        count2 = 0
        start = 0
        scopus_search()

        while total >= count2:

            scopus_search()
            count = 0
            link = []
            date0 = []

            while count < 25:
                try:
                    link.append(data["search-results"]["entry"][count]["link"][2]['@href'])
                    date0.append(data["search-results"]["entry"][count]["prism:coverDate"])
                    linky=link[0]
                    date = date0[0]
                    print(date)
                    print(linky)
                except:
                    print("You have encountred an eror")
                try:
                    get_abstractdc(linky)
                except:
                    print("The Scopus has no Abstract Available")
                count += 1
                count2 += 1
                start += 1
                link=[]
                date0=[]
                print("{} of {}".format(start,total))

                if count2 >= total:
                    api_index = 0
                    start_date += 1
                    total = 0
                    count = 25
            json.dump(data, allfile, indent=2)
            allfile.flush()

            api_index += 25
            if total - count2 == 25:
                api_index = total - 25
            if start == 4975:
                start_date += 1
                api_index = 0
                scopus_search()
                count2 = 0

    print("Scopus Text Mining & Webscraping are Complete")