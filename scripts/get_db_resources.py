from requests import get
import requests
import pickle
from tqdm import tqdm

with open('country_map.p', 'rb') as handle:
    c_map = pickle.load(handle)

with open('institution_map.p', 'rb') as handle:
    i_map = pickle.load(handle)

with open('journal_map.p', 'rb') as handle:
    j_map = pickle.load(handle)

def change_uri(uri):
    resource = uri.rsplit('/', 1)[-1]
    return "http://dbpedia.org/data/"+resource+".ntriples", resource


def download(uri):
    url, res = change_uri(uri)
    filename = "triple_data/"+res+".nt"
    # open in binary mode
    with open(filename, "w") as file:
        # get request
        response = get(url)
        # write to file
        if response.text.startswith('<'):
            file.write(response.text.encode("utf-8").decode("ISO-8859-1", "ignore"))
        else:
            print('file error for:', url)

for keys in tqdm(c_map):
    download(c_map[keys])

for keys in tqdm(j_map):
    download(j_map[keys])

for keys in tqdm(i_map):
    download(i_map[keys])
