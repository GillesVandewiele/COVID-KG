import json
import sys

with open(sys.argv[1]) as json_file:
    data = json.load(json_file)

with open(sys.argv[2], "w") as jsonFile:
    json.dump(data, jsonFile, indent=4, sort_keys=True)
