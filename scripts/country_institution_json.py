import json
import sys
import requests
import urllib.parse
from Levenshtein import ratio
import pickle
import glob
from tqdm import tqdm
import os
from multiprocessing import Pool
import pickle


with open('country_map.p', 'rb') as handle:
    c_map = pickle.load(handle)

with open('institution_map.p', 'rb') as handle:
    i_map = pickle.load(handle)


def process(file):
    with open(file) as json_file:
        data = json.load(json_file)
        ats = []
        counter = 1
        for author in data['metadata']['authors']:
            author['author_number'] = str(counter)
            counter += 1
            if 'location' in author['affiliation']:
                if 'country' in author['affiliation']['location']:
                    if author['affiliation']['location']['country'] in c_map:
                        author['db_country'] = c_map[author['affiliation']['location']['country']]
                        #print(c_map[author['affiliation']['location']['country']])
            if 'institution' in author['affiliation']:
                if author['affiliation']['institution'] in i_map:
                    author['db_institution'] = i_map[author['affiliation']['institution']]
            ats.append(author)
        data['metadata']['authors'] = ats
        data['full_text'] = ' '.join([x['text'] for x in data['body_text']])
            #print(author['affiliation']['location']['country'])

    with open("output_country_institution/"+os.path.basename(file), "w") as jsonFile:
        json.dump(data, jsonFile, indent=4, sort_keys=True)


files = glob.glob("output/*.json")
with Pool(10) as pool:
    list(tqdm(pool.imap_unordered(process, files), total=len(files)))



# with open(sys.argv[1]) as json_file:
#     data = json.load(json_file)
#     refs = []
#     for d in data['bib_entries']:
#         bibref = data['bib_entries'][d]
#         bibref['key'] = d
#
#         if 'DOI' not in bibref['other_ids']:
#             n_doi = request_doi(bibref['title'])
#             if n_doi is not None:
#                 bibref['other_ids']['DOI'] = n_doi
#                 print('added DOI:', n_doi, 'for', bibref['title'])
#         refs.append(bibref)
#     data['bib_entries'] = refs
#
# with open('requests.pkl', 'wb') as handle:
#     pickle.dump(request_map, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
#
# with open(sys.argv[2], "w") as jsonFile:
#     json.dump(data, jsonFile, indent=4, sort_keys=True)
