import json
from urllib.request import urlopen

import time
import requests

api_key = '97268ece001b743d88289c0319265c53'
headers = {
    "Accept": "application/json",
    "X-ELS-APIKey": api_key,
}


def get_abstractdc(SCOPUS_ID): ### he only use this at query scopus and get abstract
    url_abstract = ("http://api.elsevier.com/content/abstract/scopus_id/" + SCOPUS_ID)
    resp = requests.get(url_abstract, headers={'Accept':'application/json', 'X-ELS-APIKey': api_key})

    return json.loads(resp.text.encode('utf-8'))


topic_research = open('keyword.txt', 'r')

url = "https://api.elsevier.com/content/search/scopus?&count=25"
# url = "https://api.elsevier.com/content/search/scidir?query=DOI%28%2210.1021%2Fes052595%2B%22%29"


# print(data)
# print(json.dumps(data, indent=2))

# print('test')
count = 1
finish = 10
api_index=0
start_index = 1
while (count < finish):
    topic = topic_research.readline().strip()
    keyword = topic
    print(keyword)
    api_update= api_key[api_index]
    api_index+=1
    query_scopus = {}
    query_scopus["query"] = keyword
    # query_scopus["date"] = str(date_int) + "-" + str(date_int + period)  # the date range associated with the search
    # query_scopus["count"] = count  # items per page
    query_scopus["start"] = start_index
    # query_scopus["sort"] = "citedby-count"

    response = requests.get(url, params=query_scopus, headers=headers)
    data = response.json()
    
    print(query_scopus['query'])
    if topic == '':
        break
    for coverDate in data['search-results']["opensearch:totalResults"]:
        response = requests.get(url, params=query_scopus, headers=headers)
        
        data = response.json()
        totalResults = data["search-results"]["opensearch:totalResults"]
        total = int(totalResults)
        print(total)
        end_index = total
        # title = coverDate['dc:title']
        print(len(data['search-results']))
        scopusidlist = []

        while(end_index > api_index):

            query_scopus = {}
            query_scopus["query"] = keyword
            # query_scopus["date"] = str(date_int) + "-" + str(date_int + period)  # the date range associated with the search
            # query_scopus["count"] = count  # items per page
            query_scopus["start"] = api_index

            try:
                request_scopus = requests.get(url,api_index, params=query_scopus,
                                              headers={'Accept': 'application/json',
                                                       'X-ELS-APIKey': api_update})
            except:
                print("except request")

            try:
                for i in data["search-results"]["entry"]:
                    scopusidlist.append(i["dc:identifier"])
            except:
                    print("error in dc:identifier")
            print(scopusidlist)
            for sid in scopusidlist:
                
                results = get_abstractdc(sid)
                title = results['abstracts-retrieval-response']['coredata']['dc:title'].encode('utf-8').decode('utf-8')
                print('{}: title: {}'.format(count,title))
                count += 1
                journal = results['abstracts-retrieval-response']['coredata']['prism:publicationName'].encode('utf-8').decode('utf-8')
                # abstract = results['abstracts-retrieval-response']['coredata']['dc:description'].encode('utf-8').decode('utf-8')
                        # print('abstract: {}'.format(abstract.decode('utf-8')))
                json_string = json.dumps(journal)
                try:
                    text_file = open ("textmining.txt", "w")
                    text_file.write('{}\t{}\n'.format(title, journal))
                    print(api_index)
                    api_index+=1
                finally:
                    text_file.close()
                # with open ("textmining.txt", "w") as text_file:
                    
                #     text_file.write('{}\t{}\n'.format(title, journal))
                    # text_file.flush()
                    # except:
                    #     print('sid:{} error'.format(sid))
            count=count+1
        # date = coverDate['prism:coverDate']
        # keywords = coverDate['authkeywords']
        # print(title, date)

        # json_string = json.dumps(data)
        # with open("textmining.txt", "w") as text_file:
        #     text_file.write(json_string)
            

