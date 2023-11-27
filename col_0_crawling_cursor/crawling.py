import requests
import json
import time

def get_abstractdc(SCOPUS_ID): ### he only use this at query scopus and get abstract
    url_abstract = ("http://api.elsevier.com/content/abstract/scopus_id/" + SCOPUS_ID)
    resp = requests.get(url_abstract, headers={'Accept':'application/json', 'X-ELS-APIKey': elsevier_api_key})

    return json.loads(resp.text.encode('utf-8'))


topics_f = open('topics_keywords.txt', 'r')
#api_key is made in https://dev.elsevier.com/
api_key = '97268ece001b743d88289c0319265c53'
url_scopus = 'http://api.elsevier.com/content/search/scopus'
api_index = 0
period = 2
end_date = 2019
end_index = 5000 #this value doesn't change
count = 200 #For this time it only has 25 limit
cnt = 1
while(True):
    topic = topics_f.readline().strip()
    if topic == '':
        break
    print(topic)
    elsevier_keyword = topic
    date_int = 2000
    elsevier_api_key = api_key[api_index]
    api_index += 1
    start_index = 1

    while date_int <= end_date:
        if topic == 'Autonomous Systems':
            if date_int == 2017:
                date_int += period
                continue
        start = time.time()
        print(date_int)

        query_scopus = {}
        query_scopus["query"] = elsevier_keyword
        query_scopus["date"] = str(date_int) + "-" + str(date_int + period)  # the date range associated with the search
        query_scopus["count"] = count  # items per page
        query_scopus["start"] = start_index
        query_scopus["sort"] = "citedby-count"
        print(query_scopus["query"])
        try:
            request_scopus = requests.get(url_scopus, params=query_scopus,
                                    headers={'Accept': 'application/json',
                                    'X-ELS-APIKey': elsevier_api_key})
            d_scopus = request_scopus.json()
            totalResults = d_scopus["search-results"]["opensearch:totalResults"]
            total = int(totalResults)
            print(total)
            if total < end_index:
                end_index = total
        except:
            print("except request")


        output_f = open('crawl/{}_{}.txt'.format(topic, date_int), 'w')
        #output_f = open('output/test.txt'.format(topic, date_int), 'w')
        while(start_index<end_index): #--------------------------------------The start index keeps +1 until 5000 so it will loop 5000x

            query_scopus = {}
            query_scopus["query"] = elsevier_keyword
            query_scopus["date"] = str(date_int) + "-" + str(date_int + 1)  # the date range associated with the search
            query_scopus["count"] = count  # items per page
            query_scopus["start"] = start_index
            query_scopus["sort"] = "citedby-count"
            
            try:
                request_scopus = requests.get(url_scopus, params=query_scopus,
                                              headers={'Accept': 'application/json',
                                                       'X-ELS-APIKey': elsevier_api_key})
            except:
                print("except request")
            d_scopus = request_scopus.json()

            scopusid_list = []
            # print(start_index)
            try:
                for i in d_scopus["search-results"]["entry"]:
                    scopusid_list.append(i["dc:identifier"])
            except:
                print("error in dc:identifier")

            for sid in scopusid_list:
                try:
                    results = get_abstractdc(sid)
                    title = results['abstracts-retrieval-response']['coredata']['dc:title'].encode('utf-8').decode('utf-8')
                    print('{}: title: {}'.format(cnt,title))
                    cnt += 1
                    journal = results['abstracts-retrieval-response']['coredata']['prism:publicationName'].encode('utf-8').decode('utf-8')
                    abstract = results['abstracts-retrieval-response']['coredata']['dc:description'].encode('utf-8').decode('utf-8')
                    # print('abstract: {}'.format(abstract.decode('utf-8')))
                    output_f.write('{}\t{}\t{}\n'.format(title, journal, abstract))
                    output_f.flush()
                except:
                    print('sid:{} error'.format(sid))
            start_index += count
        output_f.close()

        date_int += period
        print('time: {}'.format(time.time()-start))
