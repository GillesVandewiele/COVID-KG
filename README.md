# Generating a Knowledge Graph of COVID-19 Literature

| Section | Description |
|-|-|
| [Installing](#installing-the-requirements) | Installing the requirements |
| [Downloading](#downloading-the-data) | Downloading the data |
| [Preparing](#preparing-the-jsons) | Preparing the JSONs |
| [Running](#running-rml) | Running RML |
| [Querying](#linked-data-fragments-endpoint) | Linked Data Fragments endpoint |
| [Analyzing](#knowledge-graph-applications) | Knowledge Graph Applications |

## Installing the requirements

Generating the COVID KG requires a few dependencies. Firstly, Python 3 should be installed with the following libraries:
```
SPARQLWrapper
nltk
numpy
pandas
requests
scipy
sklearn
tqdm
```

Further, to run RML, you will need:
* to have a recent version of Node.js and install the following dependency: `npm i @rmlio/yarrrml-parser -g`
* a recent Java version, and [RMLMapper](https://github.com/RMLio/rmlmapper-java)

## Downloading the data

The dataset can be retrieved from [Kaggle](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge). After downloading the dataset, re-arrange the files to have the following directory structure:
```
data
|-metadata.csv
|-papers
  |-<PAPER_1>.json
  |-...
  |-<PAPER_N>.json
```

## Preparing the JSONs

### Create a sample dataset (OPTIONAL)
Make sure you have a directory called `sample` with a `papers` directory in there. Then run `python3 scripts/generate_sample_data`.

### Create bag of words of the content
To create a bag of words for title, abstract and body, run `python3 scripts/create_bow.py <INPUT_DIR> <OUTPUT_DIR>`. As an example, you could run: `python3 scripts/create_bow.py sample output`.

### Mapping the string representations to known resources
Run `python3 scripts/map_entities.py <INPUT_DIR> <OUTPUT_DIR>` to generate different pickled dictionaries with the following structure: `{string: URI}`.

Run `python3 scripts/get_db_resources.py <INPUT_DIR> <OUTPUT_DIR>` to get the dbpedia ntriple files of the known resources. The <INPUT_DIR> is usually the previous script <OUTPUT_DIR>.

### Change the json representation and add links to known resources
To add the information of the known resources in the paper's json representation, run `python3 scripts/ountry_institution_json.py <INPUT_DIR> <PICKLE_DIR> <OUTPUT_DIR>`. Iteratively, this script will add the country and institution external links to the json dictionaries of all files in the INPUT_DIR.

### Change the metadata csv and add links to known resources
To add the external links to the metadata.csv file run `python3 scripts/csv_transform.py <INPUT_DIR> <PICKLE_DIR> <OUTPUT_DIR>`. This script will add an additional column with the journal dbpedia link.

## Running RML

<p align="center">
  <img src="images/rml.png">
</p>

After preparing the JSONs, we can convert them to RDF using RML. 
The `python3 scripts/loop.py <INPUT_DIR> <JOBS>` script shows how this transformation can be performed in python, using external commands:
```
yarrrml-parser -i rules.yml -o rules.rml.ttl
java -jar /path/to/rmlmapper.jar -m rules.rml.ttl
``` 

In this script, all json files from the INPUT_DIR are first copied to the tmp/ folder. This is the source entrypoint defined by our yarrrml script. You can change this location by changing the sources in the `rule.yml` file.
This conversion can be exectued in parallel and the <JOBS> parameter is defined to indicute how many thread can be used at the same time.
  
Analogue, the metadata.csv and bow.json can be transformed to RDF by using the corresponding yml files in the RML folder.
```
yarrrml-parser -i mapping-csv.yml -o csv.rml.ttl
java -jar /path/to/rmlmapper.jar -m csv.rml.ttl -o <DIR>/metadata.nt
```

```
yarrrml-parser -i mapping-bow.yml -o csv.rml.ttl
java -jar /path/to/rmlmapper.jar -m csv.rml.ttl -o <DIR>bow.nt
``` 

### Create KG
Executing all these rmlmapper commands result in a large set of `.nt` files. All of them were combined in one sigle file to represent the KG.
Simply concat them using the following bash command:
```
for i in *.nt;do cat $i >> kg.nt;done
```

## Linked Data Fragments endpoint

We are hosting an endpoint that can be used for querying [here](https://query-covid19.linkeddatafragments.org/). The corresponding repository for this can be found [here](https://github.com/rubensworks/covid19-web-query-client).

<p align="center">
  <img src="images/ldf.png">
</p>

## Knowledge Graph Applications

# Citation

In case you use the COVID-KG in research, we would appreciate citations!
```bibtex
@inproceedings{covid_kg,
  title={Facilitating COVID-19 Meta-analysis Through a Literature Knowledge Graph},
  author={Bram Steenwinckel and Gilles Vandewiele and
          Ilja Rausch and Pieter Heyvaert and 
          Pieter Colpaert and Pieter Simoens and
          Anastasia Dimou and Filip De Turkc and
          Femke Ongenae},
  booktitle={Accepted in Proc. of 19th International Semantic Web Conference (ISWC)},
  year={2020}
}
```

# Acknowledgements

This has been a collaboration between a lot of people:
* [Bram Steenwinckel](https://bsteenwi.github.io/)
* [Pieter Heyvaert](https://pieterheyvaert.com/)
* Michael Weyns
* Anastasia Dimou
* [Pieter Colpaert](https://pietercolpaert.be/)
* [Ruben Taelman](https://www.rubensworks.net/)
* Ruben Dedecker
* [Dylan Van Assche](https://www.dylanvanassche.be/)
* Femke Ongenae

<p align="center">
  <img src="images/idlab.png">
</p>
