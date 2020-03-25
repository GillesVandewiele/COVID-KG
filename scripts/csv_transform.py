import pandas as pd
import pickle

with open('journal_map.p', 'rb') as handle:
    i_map = pickle.load(handle)

df = pd.read_csv('metadata.csv')
df['journal_uri'] = df['journal'].apply(lambda x: i_map[x] if x in i_map else '')
df.to_csv('meta_journal_update.csv')
