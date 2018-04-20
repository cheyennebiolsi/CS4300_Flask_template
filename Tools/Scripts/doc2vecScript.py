import csv
import sys
import os
from gensim.models import Doc2Vec
sys.path.insert(0, os.path.abspath('..'))
from Serializable.SerializableToModel import SerializableToModelConverter

converter = SerializableToModelConverter()
serializedJsonFileName = sys.argv[1] #just get it from command line arguments
data = converter.convertFromFile(serializedJsonFileName)
taggedDocuments = []
for animeDocument in data:
    taggedDocuments.append(animeDocument.toTaggedDocument())
print(len(taggedDocuments))
model = Doc2Vec(vector_size=300, window=20, min_count=5, alpha=0.025, min_alpha=0.025, workers=4)
model.build_vocab(taggedDocuments)
print("done building vocab")
model.train(taggedDocuments, total_examples=model.corpus_count, epochs=model.iter)
model.save('doc2vec.model')
#header = ["anime_id"] + [genre.genre_name for genre in sorted(data[0].getGenreDictionary().keys(), key = lambda genre : genre.genre_id)]
#with open("tags_anime_documents.csv", "w+") as csvFile:
#    writer = csv.writer(csvFile)
#    writer.writerow(header)
#    for animeDocument in data:
#        row = [animeDocument.anime_id] + animeDocument.getGenreVector()
#        writer.writerow(row)
