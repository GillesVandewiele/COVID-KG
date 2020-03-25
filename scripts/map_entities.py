"""
Map the string representation of different entities to known resources
such as DBpedia
"""

import os
import json
import sys
import pickle
import requests
import urllib

import numpy as np
import pandas as pd

from SPARQLWrapper import SPARQLWrapper, JSON
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

DATA_DIR = sys.argv[1]
OUTPUT_DIR = sys.argv[2]


def try_url(x):
    """Replace spaces by underscores and check whether its a valid URI"""
    x = urllib.parse.quote_plus(x.replace(' ', '_'))
    url = 'http://dbpedia.org/resource/{}'.format(x)
    try:
        response = requests.get(url, headers={'Connection': 'close'})
        status = response.status_code
        if status == 200:
            return response.url.replace('/page/', '/resource/')
        else:
            return None
    except Exception as e:
        return None


def check_country(country):
    if country is None:
        return False
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        ASK { 
            <"""+country+"""> a dbo:Country .
        }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results['boolean']:
        return True
    else:
        return False


def check_journal(journal):
    if journal is None:
        return False
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        ASK { 
            <"""+journal+"""> a dbo:AcademicJournal .
        }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results['boolean']:
        return True
    else:
        return False


def check_institution(institution):
    if institution is None:
        return False
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        ASK { 
            <"""+institution+"""> a dbo:EducationalInstitution .
        }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results['boolean']:
        return True
    else:
        return False

# Load our data
datafiles = []
for dirname, _, filenames in os.walk('{}/papers'.format(DATA_DIR.strip('/'))):
    for filename in filenames:
        ifile = os.path.join(dirname, filename)
        if ifile.split(".")[-1] == "json":
            datafiles.append(ifile)
meta = pd.read_csv('{}/metadata.csv'.format(DATA_DIR.strip('/')))

print('Loaded {} papers!'.format(len(datafiles)))

# Map all unique country strings to DBpedia resources
countries = set()
for file in tqdm(datafiles):
    data = json.loads(open(file, 'r').read())
    for author in data['metadata']['authors']:
        if ('affiliation' in author
          and 'location' in author['affiliation']
          and 'country' in author['affiliation']['location']):
            countries.add(author['affiliation']['location']['country'])
print('Mapping {} countries!'.format(len(countries)))

country_map = {}
for country in tqdm(countries, total=len(countries)):
    if pd.isnull(country):
        continue

    url = try_url(country)
    if check_country(url):
        country_map[country] = url

print('Mapped {} countries in total!'.format(len(country_map)))
pickle.dump(country_map, open('{}/country_map.p'.format(OUTPUT_DIR.strip('/')), 
							  'wb+'))

# Map all unique journal names to DBpedia resources
journals = set(meta['journal'])
print('Mapping {} journals!'.format(len(journals)))

journal_map = {}
for journal in tqdm(journals, total=len(journals)):
    if pd.isnull(journal):
        continue
 
    url = try_url(journal)
    if check_journal(url):
        journal_map[journal] = url

print('Mapped {} journals in total!'.format(len(journal_map)))
pickle.dump(journal_map, open('{}/journal_map.p'.format(OUTPUT_DIR.strip('/')), 
							  'wb+'))

# Map all unique institution names to DBpedia resources
institutions = set()
for file in tqdm(datafiles):
    data = json.loads(open(file, 'r').read())
    for author in data['metadata']['authors']:
        if 'affiliation' in author and 'institution' in author['affiliation']:
            institutions.add(author['affiliation']['institution'])
print('Mapping {} institutions!'.format(len(institutions)))

institution_map = {}
for institution in tqdm(institutions, total=len(institutions)):
    if pd.isnull(institution):
        continue
        
    url = try_url(institution)
    if check_institution(url):
        institution_map[institution] = url

print('Mapped {} institutions in total!'.format(len(institution_map)))
pickle.dump(institution_map, open('{}/institution_map.p'.format(OUTPUT_DIR.strip('/')), 
							      'wb+'))