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


#api_key is made in https://dev.elsevier.com/
q = queue.Queue()
# need to get api key in scopus api web and add it into api_key array
api_key = [
'2b47a98595e982a0cc22e5bb451db65c',
'cffb3fbc4171813fcd8c9e5976f3c294',
'4555dd923cc93da283012a4004ab9ae4',
'3788872bebb135ffc8012cf6d241fe10',
'5a4e966495fe08e51a2e5b76e007a033',
'd9260983e502b9231e59a532b730a268',
'8a2239503ae69122ba73aad4ff43f6a6',
'd13778cbea7b3d835f7f7ef4e9c4e491',
'04c01f53daebcb1d34aa07c44cea5e39',
'08738523c321471c6dd08245e3378199'
]
# 	Website URL	Label	API Key

for item in api_key:
    q.put(item)
    #print(item)
url_scopus = 'http://api.elsevier.com/content/search/scopus'

date_int = 1999
end_date = 2020

count = 200
elsevier_api_key = q.get()
q.task_done()
print('test:'+elsevier_api_key)

journals = []
j_f = codecs.open('crawl/ref/1000-source-results.csv','r','utf-8')
while True:
    journal = j_f.readline().strip()
    if journal =="":
        break
    journals.append(journal)

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



cnt = 1
j_cnt = 1

# topic = 'TITLE-ABS-KEY("autonomous system"+OR+"autonomous vehicle")AND(EXACTSRCTITLE("Autonomous Robots"))'
topic = 'TITLE-ABS-KEY("autonomous system"+OR+"autonomous vehicle")'

# elsevier_keyword = topic

for journal in journals:
    print(str(j_cnt)+':'+journal)
    j_cnt = j_cnt + 1
    cursor = '*'
    elsevier_keyword = topic + 'AND(EXACTSRCTITLE("'+journal+'"))'
    current = 0
    while True:
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
            print(d_scopus)
            total = d_scopus["search-results"]["opensearch:totalResults"]
            current = current + 200

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


                # affiliation = results['abstracts-retrieval-response']['affiliation']
                # if isArray(str(affiliation)):
                #     authors = results['abstracts-retrieval-response']['authors']['author']
                #     if isArray(str(authors)):
                #         for author in authors:
                #             if author['@seq']=='1':
                #                 if isArray(str(author['affiliation'])):
                #                     affiliation_id = author['affiliation'][0]['@id']
                #                 else:
                #                     affiliation_id = author['affiliation']['@id']
                #     else:
                #         if isArray(str(results['abstracts-retrieval-response']['authors']['author']['affiliation'])):
                #             affiliation_id = results['abstracts-retrieval-response']['authors']['author']['affiliation'][0]['@id']
                #         else:
                #             affiliation_id = results['abstracts-retrieval-response']['authors']['author']['affiliation']['@id']
                #     # print('{}: affiliation: {}'.format(cnt, affiliation))
                #     for aff in affiliation:
                #         if aff['@id'] == affiliation_id:
                #             affiliation_country = aff['affiliation-country']
                #             break
                #
                # else:
                #     affiliation_country = affiliation['affiliation-country']
                # affiliation_country = affiliation_country.encode('utf-8').decode('utf-8')
                # print('{}: affiliation_country: {}'.format(cnt, affiliation_country))


                # output_f = open('crawl/{}/{}.txt'.format(filename, year[:4]), 'a', 'utf-8')
                output_f = codecs.open('crawl/{}/{}.txt'.format('autonomous', year[:4]), 'a', 'utf-8')
                output_f.write('{}\t{}\t{}\t{}\t'
                               '{}\t{}\t{}\t{}\t'
                               '{}\t{}\t{}\t{}\n'.format(
                    title, year[:4], journal, abstract,
                    aggregationType, srctype, subtype, subtypeDescription,
                    "affiliation_country", citedby_count, subjects, paper_keywords))
                output_f.flush()
                output_f.close()
                cnt += 1
            except Exception as e:
                print('sid:{} error'.format(sid), e)

        if current >= int(total):
            break
    # print('time: {}'.format(time.time()-start))
