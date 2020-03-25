#!/bin/bash
name=$(echo ${1##*/} | cut -f 1 -d '.')
python transform_json.py $1 tmp/transform_data.json
yarrrml-parser -i mapping.yml -o tmp/mapping.rml.ttl
java -jar rmlmapper-4.4.1-r96.jar -m tmp/mapping.rml.ttl -o output/meta_triples_$name.nt
