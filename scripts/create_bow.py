"""
Create bag of words for titles, bodies and abstracts of the papers
"""

import os
import json
import sys

import numpy as np
import pandas as pd

from scipy.sparse import find
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

import nltk
from nltk.corpus import stopwords

DATA_DIR = sys.argv[1]
OUTPUT_DIR = sys.argv[2]

# Load our data
datafiles = []
sha_to_file = {}
file_to_sha = {}
for dirname, _, filenames in os.walk('{}/papers'.format(DATA_DIR.strip('/'))):
    for filename in filenames:
        ifile = os.path.join(dirname, filename)
        if ifile.split(".")[-1] == "json":
            datafiles.append(ifile)
            sha_to_file[ifile.split('/')[-1].split('.')[0]] = ifile
            file_to_sha[ifile] = ifile.split('/')[-1].split('.')[0]

meta = pd.read_csv('{}/metadata.csv'.format(DATA_DIR.strip('/')))
meta = meta[~pd.isnull(meta['doi'])]
sha_to_doi = {}
doi_to_sha = {}
for i, row in meta.iterrows():
    sha_to_doi[row['sha']] = row['doi'].strip('http://dx.doi.org/')
    doi_to_sha[row['doi'].strip('http://dx.doi.org/')] = row['sha']

print('Loaded {} papers!'.format(len(datafiles)))

# Create dataframe with the raw texts
paper_metadata = []
for file in tqdm(datafiles):
    if file in file_to_sha and file_to_sha[file] in sha_to_doi:
        data = json.loads(open(file, 'r').read())
        body = ' '.join([x['text'] for x in data['body_text']])
        abstract = ' '.join([x['text'] for x in data['abstract']])
        title = data['metadata']['title']
        vector = [sha_to_doi[file_to_sha[file]], title, abstract, body]
        paper_metadata.append(vector)
cols = ['id', 'title', 'abstract', 'body']
metadata_df = pd.DataFrame(paper_metadata, columns=cols)

# Fit bag-of-words models
custom_words = {
	'doi', 'preprint', 'copyright', 'peer', 'reviewed', 'org', 'https', 
	'et', 'al', 'author', 'figure', 'rights', 'reserved', 'permission', 
	'used', 'using', 'biorxiv', 'fig', 'fig.', 'al.', 'di', 'la', 'il', 
	'del', 'le', 'della', 'dei', 'delle', 'una', 'da',  'dell',  'non', 'si',
	'table', 'like', 'do', 'does'
}
custom_words = custom_words.union(set(map(str, range(1, 2000))))
custom_stopwords = list(set(stopwords.words('english')).union(custom_words))
title_vectorizer = CountVectorizer(max_features=250, binary=True, 
								   stop_words=custom_stopwords)
abstract_vectorizer = CountVectorizer(max_features=250, binary=True, 
								     stop_words=custom_stopwords)
body_vectorizer = CountVectorizer(max_features=250, binary=True, 
								  stop_words=custom_stopwords)
title_bow = title_vectorizer.fit_transform(metadata_df['title'])
abstract_bow = abstract_vectorizer.fit_transform(metadata_df['abstract'])
body_bow = body_vectorizer.fit_transform(metadata_df['body'])

# Create dataframes with the bag of words
inv_title_voc = {}
for k, v in title_vectorizer.vocabulary_.items():
    inv_title_voc[v] = k
    
inv_abstract_voc = {}
for k, v in abstract_vectorizer.vocabulary_.items():
    inv_abstract_voc[v] = k
    
inv_text_voc = {}
for k, v in body_vectorizer.vocabulary_.items():
    inv_text_voc[v] = k

title_bows = []
for doi, bow in tqdm(zip([x[0] for x in paper_metadata], title_bow), 
					 total=len(paper_metadata)):
	title_bows.append(list(bow.toarray()[0]) + [doi, doi_to_sha[doi]])
title_df = pd.DataFrame(title_bows)
title_df.columns = [inv_title_voc[k] for k in range(len(title_vectorizer.vocabulary_))] + ['doi', 'sha']
title_df.to_csv('{}/title_bow.csv'.format(OUTPUT_DIR))

abstract_bows = []
for doi, bow in tqdm(zip([x[0] for x in paper_metadata], abstract_bow), 
					 total=len(paper_metadata)):
	abstract_bows.append(list(bow.toarray()[0]) + [doi, doi_to_sha[doi]])
abstract_df = pd.DataFrame(abstract_bows)
abstract_df.columns = [inv_abstract_voc[k] for k in range(len(abstract_vectorizer.vocabulary_))] + ['doi', 'sha']
abstract_df.to_csv('{}/abstract_bow.csv'.format(OUTPUT_DIR))

body_bows = []
for doi, bow in tqdm(zip([x[0] for x in paper_metadata], body_bow), 
					 total=len(paper_metadata)):
	body_bows.append(list(bow.toarray()[0]) + [doi, doi_to_sha[doi]])
body_df = pd.DataFrame(body_bows)
body_df.columns = [inv_text_voc[k] for k in range(len(body_vectorizer.vocabulary_))] + ['doi', 'sha']
body_df.to_csv('{}/body_bow.csv'.format(OUTPUT_DIR))
