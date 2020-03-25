# Generating a Knowledge Graph of COVID-19 Literature

| Section | Description |
|-|-|
| [Installing](#installing-the-requirements) | Installing the requirements |
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


## Preparing the JSONs

### Create a sample dataset
Make sure you have a directory called `sample` with a `papers` directory in there. Then run `python3 scripts/generate_sample_data`.

### Create bag of words of the content
To create a bag of words for title, abstract and body, run `python3 scripts/create_bow.py <INPUT_DIR> <OUTPUT_DIR>`. As an example, you could run: `python3 scripts/create_bow.py sample output`.

### Mapping the string representations to known resources
Run `python3 scripts/map_entities.py <INPUT_DIR> <OUTPUT_DIR>` to generate different pickled dictionaries with the following structure: `{string: URI}`.

## Running RML

<p align="center">
  <img src="images/rml.png">
</p>

After preparing the JSONs, we can convert them to RDF using RML. To do this, run:
```
yarrrml-parser -i rules.yml -o rules.rml.ttl
java -jar /path/to/rmlmapper.jar -m rules.rml.ttl
``` 

## Linked Data Fragments endpoint

We are hosting an endpoint that can be used for querying [here](https://query-covid19.linkeddatafragments.org/). The corresponding repository for this can be found [here](https://github.com/rubensworks/covid19-web-query-client).

<p align="center">
  <img src="images/ldf.png">
</p>

## Knowledge Graph Applications

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