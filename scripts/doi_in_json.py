import pandas as pd
import json
import glob
import numpy as np
import requests
from tqdm import tqdm
import urllib

from multiprocessing.pool import ThreadPool


df = pd.read_csv('metadata.csv')

af = df[['sha', 'doi']].values
headers = {'User-Agent': 'covid_data (mailto:bram.steenwinckel.com)'}


def get_data(a):
    try:
        sha, doi = a
        if len(doi) > 2:
            q = urllib.parse.quote(doi)
            response = requests.get("https://api.crossref.org/works/"+q, headers=headers)
            data = response.json()
            with open('cross_ref_data/'+urllib.parse.quote(doi, safe='')+".json", 'w') as outfile:
                json.dump(data, outfile)
    except Exception as e:
        print(e)


with ThreadPool(10) as pool:
    list(tqdm(pool.imap_unordered(get_data, af), total=len(af)))




# files = glob.glob("output/*.json")
# for file in files:
#     with open(file) as json_file:
#         data = json.load(json_file)
#         try:
#             doi = df[df.sha == data['paper_id']]['doi'].values[0]
#             doi = remove_prefix(doi, 'http://dx.doi.org/')
#             doi = remove_prefix(doi, 'doi.org/')
#             data['paper_doi'] = doi
#             print(data['paper_doi'])
#         except Exception as e:
#             print(e)
#         input()
