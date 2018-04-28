import csv
import sys
import os
import json
sys.path.insert(0, os.path.abspath('..'))
from Serializable.SerializableToModel import SerializableToModelConverter

converter = SerializableToModelConverter()
fileName = sys.argv[1]
videoUrlsCsv = sys.argv[2]
data = converter.convertFromFile(fileName)
attributes = ["anime_id", "anime_index", "anime_english_title", "anime_image_url", "anime_synopsis"]
result = []
videoUrlDict = {}
with open(videoUrlsCsv, "rb") as videocsv:
        reader = csv.DictReader(videocsv)
        for row in reader:
            anime_id = row["anime_id"]
            if not anime_id.isdigit():
                print("Skipping: {}".format(anime_id))
                continue
            anime_id = int(anime_id)
            anime_video_url = row["anime_video_url"]
            if "not available" in anime_video_url:
                videoUrlDict[anime_id] = "none"
            else:
                videoUrlDict[anime_id] = anime_video_url
for document in data:
    dictionary = {attribute:getattr(document, attribute) for attribute in attributes}
    anime_id = int(dictionary["anime_id"])
    if anime_id in videoUrlDict:
        dictionary["anime_video_url"] = videoUrlDict[anime_id]
    else:
        dictionary["anime_video_url"] = "none"
    result.append(dictionary)
with open("../../app/static/data/anime_info.json", "w+") as jsonFile:
    json.dump(result, jsonFile)
  
