import glob
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
import multiprocessing
import threading
import json
import os
import subprocess
from multiprocessing import Pool

files = glob.glob("output_country_institution/*.json")


def process_and_map(file):
    id = threading.current_thread().name[len('Thread-'):]
    #id = multiprocessing.current_process().name[len('PoolWorker-'):]
    name = os.path.basename(file)

    with open(file) as json_file:
        data = json.load(json_file)

    with open("tmp/transform_data"+id+".json", "w") as jsonFile:
        json.dump(data, jsonFile, indent=4, sort_keys=True)

    subprocess.call(['java', '-jar', 'rmlmapper-4.7.0-r150.jar', '-m', 'tmp/mapping'+id+'.rml.ttl', '-o', 'triple_data/meta_triples_'+name+'.nt'])

PROCESSES = 10
with open('mapping.yml', "r") as f:
    mapping = f.read()
for i in range(1, PROCESSES+1):
    with open('mapping'+str(i)+'.yml', 'w') as m:
        m.write(mapping.replace('transform_data.json', 'transform_data'+str(i)+'.json'))
    subprocess.call(['yarrrml-parser', '-i', 'mapping'+str(i)+'.yml', '-o', 'tmp/mapping'+str(i)+'.rml.ttl'])

with ThreadPool(10) as pool:
#with Pool(PROCESSES) as pool:
    list(tqdm(pool.imap_unordered(process_and_map, files), total=len(files)))
