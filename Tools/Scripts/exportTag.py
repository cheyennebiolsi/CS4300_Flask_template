import csv
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from Serializable.SerializableToModel import SerializableToModelConverter

converter = SerializableToModelConverter()
fileName = sys.argv[1]
data = converter.convertFromFile(fileName)
header = ["anime_id"] + [genre.genre_name for genre in sorted(data[0].getGenreDictionary().keys(), key = lambda genre : genre.genre_id)]
with open("../../data/tags_anime_documents.csv", "w+") as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(header)
    for animeDocument in data:
        row = [animeDocument.anime_id] + animeDocument.getGenreVector()
        writer.writerow(row)
