import csv
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from Serializable.SerializableToModel import SerializableToModelConverter
from Serializable.AnimeDocument import AnimeDocumentManager, AnimeDocument

converter = SerializableToModelConverter()
fileName = sys.argv[1]
animeDocuments = converter.convertFromFile(fileName)
animeDocumentManager = AnimeDocumentManager(animeDocuments)
#anime1 = animeDocumentManager.getAnimeById(20)
#res = (anime1.getAllRelatedAnime(animeDocumentManager))
#for r in res:
#    print(animeDocumentManager.getAnimeById(r).anime_english_title)

header = ["anime_id", "related_anime_id", "related_anime_title"]
with open("../../data/related_anime_documents.csv", "wb+") as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(header)
    for animeDocument in animeDocuments:
        relatedIds = animeDocument.getAllRelatedAnime(animeDocumentManager)
        relatedTitles = [animeDocumentManager.getAnimeById(anime_id).anime_english_title for anime_id in relatedIds \
                         if isinstance(animeDocumentManager.getAnimeById(anime_id), AnimeDocument)]
        relatedTitles = [unicode(s).encode("utf-8") for s in relatedTitles]
        row = [animeDocument.anime_id] + [" | ".join([str(i) for i in relatedIds])] + [" | ".join(relatedTitles)]
        writer.writerow(row)
