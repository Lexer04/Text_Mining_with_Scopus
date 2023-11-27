import json
from urllib.request import urlopen

import time
import requests

api_key = '97268ece001b743d88289c0319265c53'
headers = {
    "X-ELS-APIKey": api_key,
}

def get_abstractdc(SCOPUS_ID): ### he only use this at query scopus and get abstract
    url_abstract = ("http://api.elsevier.com/content/abstract/scopus_id/" + SCOPUS_ID)
    resp = requests.get(url_abstract, headers={'Accept':'application/json', 'X-ELS-APIKey': api_key})

    return json.loads(resp.text.encode('utf-8'))

topic_research = open('keyword.txt', 'r')
url = "https://api.elsevier.com/content/search/scopus?&count=25"

# url = "https://api.elsevier.com/content/search/scopus/" & api_index
count = 1
finish = 10
api_index=0
start_index = 1
text_file = open ("textmining.txt", "w")

while (True):
    topic = topic_research.readline().strip()
    keyword = topic
    print(keyword)
    # api_update= api_key[api_index]
    api_index+=25
    print(count)

    query_scopus = {}
    query_scopus["query"] = keyword
    query_scopus["start"] = api_index
    response = requests.get(url, params=query_scopus, headers=headers)
    print(response)
    data = response.json()
    response=[]
    print(query_scopus['query'])
    count=0
    if topic == '':
        break
    # while(count<25):
        # print('test')
    # for coverDate in data['search-results']["opensearch:totalResults"]:
        # api_index+=2
        # api_update= api_key[api_index]
        # query_scopus = {}
        # query_scopus["query"] = keyword
        # query_scopus["start"] = api_update
    response = requests.get(url, params=query_scopus, headers=headers)
    data = response.json()
    # totalResults = data["search-results"]["opensearch:totalResults"]
    # total = int(totalResults)
    # print(total)
        # T=total-count
    # end_index = total
    # print(len(data['search-results']))
    scopusidlist = []
    count = 0
    while(count < 25):
            # query_scopus = {}
            # query_scopus["query"] = keyword
            # query_scopus["start"] = api_index
            # try:
            #     request_scopus = requests.get(url, params=query_scopus,
            #                                   headers={'Accept': 'application/json',
            #                                            'X-ELS-APIKey': api_update})
            # except:
            #     print("except request")
        try:
            for i in data["search-results"]["entry"]:
                scopusidlist.append(i["dc:identifier"])
                    
        except:
            print("error in dc:identifier")
        print(scopusidlist)
            
            
        for sid in scopusidlist:
            results = get_abstractdc(sid)
            title = results['abstracts-retrieval-response']['coredata']['dc:title'].encode('utf-8').decode('utf-8')
            journal = results['abstracts-retrieval-response']['coredata']['prism:publicationName'].encode('utf-8').decode('utf-8')
            print('{}: title: {}'.format(count,title))
            count += 1
            data = []
            # json_string = json.dumps(journal)
            
            text_file.write('{}\t{}\n'.format(title, journal))
            text_file.flush()
            # try:
                
            #     title=[]
            #     journal=[]
            #     scopusidlist=[]
            # finally:
        # text_file.close()
        count=count+1
        
# data=[]
       

