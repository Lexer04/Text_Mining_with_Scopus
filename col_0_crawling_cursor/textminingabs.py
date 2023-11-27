import json
from urllib.request import urlopen

import time
import requests

api_key = '577f860d8b42100f3781010653ee10aa'
headers = {
    "X-ELS-APIKey": api_key,
}

def get_abstractdc(SCOPUS_ID): ### he only use this at query scopus and get abstract
    url_abstract = ("http://api.elsevier.com/content/abstract/scopus_id/" + SCOPUS_ID)
    resp = requests.get(url_abstract, headers={'Accept':'application/json', 'X-ELS-APIKey': api_key})

    return json.loads(resp.text.encode('utf-8'))

topic_research = open('keyword.txt', 'r')
url = "https://api.elsevier.com/content/search/scopus?&count=25"
count = 1
finish = 10
api_index=0
date = 2022
end = 2023
period = 1
start_index = 1
counttext = 0
total = 51
text_file = open ("ReinforcementLearning{}.json".format(date+1), "w")
allfile = open ("allReinforcementLearning{}.json".format(date+1), "w")

while (date <= end):
    topic = topic_research.readline().strip()
    if topic == '':
        break
        text_file.close()
        text_file = open ("textmining.txt", "w")
        topic_research = open('keyword.txt', 'r')
        topic = topic_research.readline().strip()
        print(topic)
        # date=date+period
    if total-50 < counttext:
        break
        text_file.close()
        text_file = open ("textmining.txt", "w")
        topic_research = open('keyword.txt', 'r')
        topic = topic_research.readline().strip()
        print(topic)
        date=date+period
        counttext=0
        query_scopus = []
        scopusidlist = []
    keyword = topic
    # print(keyword)
    api_index+=25
    print(date+1)
    data = []
    query_scopus = {}
    query_scopus["query"] = keyword
    query_scopus["start"] = api_index
    query_scopus["date"] = str(date) + "-" + str(date + period)
    response = requests.get(url, params=query_scopus, headers=headers)
    # print(response)
    data = response.json()
    response=[]
    # print(query_scopus['query'])
    # count=0
    
    response = requests.get(url, params=query_scopus, headers=headers)
    data = response.json()
    totalResults = data["search-results"]["opensearch:totalResults"]
    total = int(totalResults)
    print(total)
    scopusidlist = []
    count = 0
    while(count < 25):
        try:
            for i in data["search-results"]["entry"]:
                scopusidlist.append(i["dc:identifier"])
        except:
            print("error in dc:identifier")
        print(scopusidlist)
            
        for sid in scopusidlist:
            try:
                results = get_abstractdc(sid)
                title = results['abstracts-retrieval-response']['coredata']['dc:title'].encode('utf-8').decode('utf-8')
                journal = results['abstracts-retrieval-response']['coredata']['prism:publicationName']
                # abstract = results['abstracts-retrieval-response']['coredata']['dc:description'].encode('utf-8').decode('utf-8')
                scopusdate = results['abstracts-retrieval-response']['coredata']['prism:coverDate']
                # key = results['abstracts-retrieval-response']['coredata']['authkeywords'].encode('utf-8').decode('utf-8')
                scopusid = results['abstracts-retrieval-response']['coredata']['dc:identifier']
                print('{}: Date: {} title: {} + {}'.format(counttext,scopusdate,title, scopusid))
                count += 1
                print(counttext)
                # open('data_all_2013.json', "w") as allfile:
                json.dump(data, allfile, indent=2)
                allfile.flush()
            except:
                print("can't do it also")
            # data = []
            try:
                text_file.write('{}.date: {}\n{}\t{}\n scopus ID: {} \n'.format(counttext, scopusdate, title, journal, scopusid))
            except:
                print("can't do")
            counttext=counttext+1
            text_file.flush()
        count=count+1

    # date=date+period    


