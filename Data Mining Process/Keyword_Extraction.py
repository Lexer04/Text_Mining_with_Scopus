import csv
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import  keybert

filejson = "ComputerVisionStopwordsDateUpdate.json" #Name of File
count = 0
t=0
def open_json(file):
    df = pd.read_json(file)
    return df

if __name__ == '__main__':
    dfscopus = open_json(filejson)
    print(len(dfscopus))
    print(dfscopus.index)
    # print(dfscopus.loc[t]["ProcessedAbstract"])
    end = len(dfscopus)
    print(type(end))
    with open("ComputerVisionKeywordExtractionOnly.json", "w", newline='') as outfile:
        while t <= end:
            # title = dfscopus.loc[t]["Title"]
            AbstractKeyword = dfscopus.loc[t]["ProcessedAbstract"]
            # Keyword = dfscopus.loc[t]["Keyword"]
            # print(dfscopus.loc[0]["search-results"]["entry"][1]["prism:coverDisplayDate"])
            # print(dfscopus.loc[475]["search-results"]["entry"][1]["prism:coverDisplayDate"])
            # print(dfscopus[0])
            kw_model = keybert.KeyBERT()
            text = kw_model.extract_keywords(docs=AbstractKeyword, keyphrase_ngram_range=(1, 2))
            # print(text)
            t=t+1
            print("{} of {} data". format(t,end))

            scopus = {
                # 'Title':title,
                # 'Keyword':Keyword,
                'Keyword_Extraction':text,
            }

            json_object = json.dumps(scopus, indent=4)
            outfile.write(json_object)