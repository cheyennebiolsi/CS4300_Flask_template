import json
from AnimeDocument import AnimeDocument
from Review import Review

class SerializableToModelConverter:
    """
    Converts json serialized dictionaries to AnimeDocument objects
    """

    def convert(self, serialized_dict):
        """Converts a json string to an AnimeDocument object"""
        raise NotImplementedError("Let Cheyenne know if you want\n" + 
                                  "SerializableToModelConverter.convert implemented.\n" +
                                  "Use convertFromFile as alternative in the meanwhile")

    def convertFromFile(self, fileName):
        """Reads a json file and converts it to list of AnimeDocument objects"""
        with open(fileName, "r") as f:
            data = json.loads(f.readlines()[0], object_hook = self.convertAnimeDocument)
        return data 

    def convertAnimeDocument(self, serialized_dict):
        animeDocument = AnimeDocument()
        for key in serialized_dict:
            value = serialized_dict[key]
            if key == "reviews":
                for review_dict in value:
                    review = self.convertReview(review_dict)
                    animeDocument.addReview(review)
            else:
                setattr(animeDocument, key, value)
        return animeDocument
                            
    def convertReview(self, serialized_dict):
        review = Review()
        for key in serialized_dict:
            value = serialized_dict[key]
            setattr(animeDocument, key, value)
        return review 
