import csv
import sys
import os
import json
sys.path.insert(0, os.path.abspath('..'))
from Serializable.SerializableToModel import SerializableToModelConverter

converter = SerializableToModelConverter()
fileName = sys.argv[1]
data = converter.convertFromFile(fileName)
attributes = ["anime_id", "anime_index", "anime_english_title", "anime_image_url", "anime_synopsis"]
result = []
for document in data:
    dictionary = {attribute:getattr(document, attribute) for attribute in attributes}
    result.append(dictionary)
with open("../../app/static/data/anime_info.json", "w+") as jsonFile:
    json.dump(result, jsonFile)
  
