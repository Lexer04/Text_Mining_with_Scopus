import requests
import json
import time
import queue
import codecs

def isArray(str):
    if '[' in str:
        return True
    else:
        return False

topics_f = open('topics_keywords.txt', 'r')
#api_key is made in https://dev.elsevier.com/
q = queue.Queue()
# need to get api key in scopus api web and add it into api_key array
api_key = [
'5030b6475d629f8481cd1af89f187ae0',
'9713ca6b327480c333bcac6af79d3fbc',
'6e41f396b7d40a382dc08c0508c8ff5a',
'dc7baed0e121a00526bad4d7a40b5a42',
'987dabb14aacb40ea4f2891908075b7f',
'41abce7c53d62d7132fe30c57b75b319',
'524f8d78946c28e7510f9ec37c5a956c',
'021634bdc62a1f718a787edcbc4563c3',
'8e87080873e9e53b64f1a66fa8a275bb',
'1627d67c684307af2260a20fb6951651'
]
# 	Website URL	Label	API Key

for item in api_key:
    q.put(item)
    #print(item)
url_scopus = 'http://api.elsevier.com/content/search/scopus'

date_int = 2020
end_date = 2021

count = 200
elsevier_api_key = q.get()
q.task_done()
print('test:'+elsevier_api_key)


def get_abstractdc(SCOPUS_ID):
    url_abstract = ("http://api.elsevier.com/content/abstract/scopus_id/" + SCOPUS_ID)
    global elsevier_api_key
    try:
        resp = requests.get(url_abstract, headers={'Accept':'application/json', 'X-ELS-APIKey': elsevier_api_key})
        text = json.loads(resp.text.encode('utf-8'))
    except:
        if q.empty():
            print("topic: " + topic[:3])
            print("cursor: " + cursor)
            exit()
        elsevier_api_key = q.get()
        q.task_done()
        resp = requests.get(url_abstract, headers={'Accept': 'application/json', 'X-ELS-APIKey': elsevier_api_key})
        text = json.loads(resp.text.encode('utf-8'))
    return text


while(True):
    cnt = 1
    topicline = topics_f.readline().strip()
    if topicline == '':
        break
    topics = topicline.split('|')
    filename = topics[0].strip()
    topic = topics[1].strip()
    print(filename)
    # cursor = 'AoNV/MJMCEIEtr4yMi1zMi4wLTM0NTQ3NjgzNjc5'
    cursor = '*'
    # cursor = 'AoNZhfRMCEFQE6oyMi1zMi4wLTg0OTczNjAxNDI1'
    elsevier_keyword = topic

    # start = time.time()

    # query_scopus = {}
    # query_scopus["query"] = elsevier_keyword
    # query_scopus["date"] = str(date_int) + "-" + str(end_date)  # the date range associated with the search
    # query_scopus["count"] = count  # items per page
    # query_scopus["cursor"] = cursor
    #
    # try:
    #     request_scopus = requests.get(url_scopus, params=query_scopus,
    #                             headers={'Accept': 'application/json',
    #                             'X-ELS-APIKey': elsevier_api_key})
    # except:
    #     print("except request")
    #     api_index += 1
    #     if api_index >= api_key.count():
    #         print("topic: " + topic[:3])
    #         print("cursor: " + cursor)
    #         break
    # try:
    #     d_scopus = request_scopus.json()
    #     totalResults = d_scopus["search-results"]["opensearch:totalResults"]
    #     total = int(totalResults)
    #     # cursor = d_scopus["search-results"]["cursor"]["@next"]
    #     # print(str(total) + "???" + cursor)
    #     # qu = d_scopus["search-results"]["opensearch:Query"]["@searchTerms"]
    #     # print("11    "+qu)
    # except:
    #     print("parsing error")

    #output_f = open('output/test.txt'.format(topic, date_int), 'w')
    while(True):
        query_scopus = {}
        query_scopus["query"] = elsevier_keyword
        query_scopus["date"] = str(date_int) + "-" + str(end_date)  # the date range associated with the search
        query_scopus["count"] = count  # items per page
        query_scopus["cursor"] = cursor
        try:
            request_scopus = requests.get(url_scopus, params=query_scopus,
                                          headers={'Accept': 'application/json',
                                                   'X-ELS-APIKey': elsevier_api_key})

        except:
            print("except request")


            if q.empty():
                print("topic: " + filename)
                print("cursor: " + cursor)
                exit()
            elsevier_api_key = q.get()
            q.task_done()
            request_scopus = requests.get(url_scopus, params=query_scopus,
                                          headers={'Accept': 'application/json',
                                                   'X-ELS-APIKey': elsevier_api_key})


        scopusid_list = []
        # print(start_index)
        try:
            d_scopus = request_scopus.json()
            cursor = d_scopus["search-results"]["cursor"]["@next"]
            for i in d_scopus["search-results"]["entry"]:
                scopusid_list.append(i["dc:identifier"])
        except:
            print("error in dc:identifier or entry is null")
            break

        for sid in scopusid_list:
            try:
                results = get_abstractdc(sid)
                title = results['abstracts-retrieval-response']['coredata']['dc:title'].encode('utf-8').decode('utf-8')
                # print('{}: title: {}'.format(cnt,title))

                journal = results['abstracts-retrieval-response']['coredata']['prism:publicationName'].encode('utf-8').decode('utf-8')
                # print('{}: journal: {}'.format(cnt, journal))
                abstract = results['abstracts-retrieval-response']['coredata']['dc:description'].replace('©','').strip().encode('utf-8').decode('utf-8')
                # print('{}: abstract: {}'.format(cnt, abstract))
                year = results['abstracts-retrieval-response']['coredata']['prism:coverDate'].encode('utf-8').decode('utf-8')
                # print('{}: year: {}'.format(cnt, year))
                aggregationType = results['abstracts-retrieval-response']['coredata']['prism:aggregationType'].encode('utf-8').decode('utf-8')
                # print('{}: aggregationType: {}'.format(cnt, aggregationType))
                srctype = results['abstracts-retrieval-response']['coredata']['srctype'].encode('utf-8').decode('utf-8')
                # print('{}: srctype: {}'.format(cnt, srctype))
                subtype = results['abstracts-retrieval-response']['coredata']['subtype'].encode('utf-8').decode('utf-8')
                # print('{}: subtype: {}'.format(cnt, subtype))
                subtypeDescription = results['abstracts-retrieval-response']['coredata']['subtypeDescription'].encode('utf-8').decode('utf-8')
                # print('{}: subtypeDescription: {}'.format(cnt, subtypeDescription))
                citedby_count = results['abstracts-retrieval-response']['coredata']['citedby-count'].encode('utf-8').decode('utf-8')
                # print('{}: citedby-count: {}'.format(cnt, citedby_count))
                subject_areas = results['abstracts-retrieval-response']['subject-areas']['subject-area']
                subjects = 'None';
                if isArray(str(subject_areas)):
                    subjects = '';
                    tmp_index = 0
                    for subject_area in subject_areas:
                        if tmp_index == 0:
                            subjects = str(subject_area['$']).strip()
                        else:
                            subjects = subjects + "," + str(subject_area['$']).strip()
                        tmp_index = 1
                else:
                    subjects = subject_areas['$']
                # print('{}: subjects: {}'.format(cnt, subjects))

                paper_keywords = 'None';
                if results['abstracts-retrieval-response']['authkeywords'] is not None:
                    author_keywords = results['abstracts-retrieval-response']['authkeywords']['author-keyword']
                    paper_keywords = '';
                    if isArray(str(author_keywords)):
                        tmp_index = 0
                        for author_keyword in author_keywords:
                            if tmp_index == 0:
                                paper_keywords = str(author_keyword['$'])
                            else:
                                paper_keywords = paper_keywords + ',' + str(author_keyword['$'])
                            tmp_index = 1
                    else:
                        paper_keywords = str(author_keywords['$'])
                print('{}: paper_keywords: {}'.format(cnt, paper_keywords))


                affiliation = results['abstracts-retrieval-response']['affiliation']
                if isArray(str(affiliation)):
                    authors = results['abstracts-retrieval-response']['authors']['author']
                    if isArray(str(authors)):
                        for author in authors:
                            if author['@seq']=='1':
                                if isArray(str(author['affiliation'])):
                                    affiliation_id = author['affiliation'][0]['@id']
                                else:
                                    affiliation_id = author['affiliation']['@id']
                    else:
                        if isArray(str(results['abstracts-retrieval-response']['authors']['author']['affiliation'])):
                            affiliation_id = results['abstracts-retrieval-response']['authors']['author']['affiliation'][0]['@id']
                        else:
                            affiliation_id = results['abstracts-retrieval-response']['authors']['author']['affiliation']['@id']
                    # print('{}: affiliation: {}'.format(cnt, affiliation))
                    for aff in affiliation:
                        if aff['@id'] == affiliation_id:
                            affiliation_country = aff['affiliation-country']
                            break

                else:
                    affiliation_country = affiliation['affiliation-country']
                affiliation_country = affiliation_country.encode('utf-8').decode('utf-8')
                print('{}: affiliation_country: {}'.format(cnt, affiliation_country))


                # output_f = open('crawl/{}/{}.txt'.format(filename, year[:4]), 'a', 'utf-8')
                output_f = codecs.open('crawl/{}/{}.txt'.format(filename, year[:4]), 'a', 'utf-8')
                output_f.write('{}\t{}\t{}\t{}\t'
                               '{}\t{}\t{}\t{}\t'
                               '{}\t{}\t{}\t{}\n'.format(
                    title, year[:4], journal, abstract,
                    aggregationType, srctype, subtype, subtypeDescription,
                    affiliation_country, citedby_count, subjects, paper_keywords))
                output_f.flush()
                output_f.close()
                cnt += 1
            except Exception as e:
                print('sid:{} error'.format(sid), e)


    # print('time: {}'.format(time.time()-start))
