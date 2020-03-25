# Generating a Knowledge Graph of COVID-19 Literature

# Create a sample dataset
Make sure you have a directory called `sample` with a `papers` directory in there. Then run `python3 scripts/generate_sample_data`.

# Create bag of words of the content
To create a bag of words for title, abstract and body, run `python3 scripts/create_bow.py <INPUT_DIR> <OUTPUT_DIR>`. As an example, you could run: `python3 scripts/create_bow.py sample output`.

# Mapping the string representations to known resources
Run `python3 scripts/map_entities.py <INPUT_DIR> <OUTPUT_DIR>` to generate different pickled dictionaries with the following structure: `{string: URI}`.