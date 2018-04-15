import json
from Review import Review

class AnimeDocument:
    def __init__(self,
                 anime_index = "",
                 anime_id = "",
                 anime_english_title = "",
                 anime_japanese_title = "",
                 anime_image_url = "",
                 anime_genres = None,
                 anime_synopsis = "",
                 anime_rating_value = "",
                 anime_rating_count = "",
                 anime_rating = "",
                 anime_ranked = "",
                 anime_popularity = "",
                 anime_favorites = "",
                 anime_members = "",
                 anime_number_of_episodes = "",
                 anime_type = "",
                 anime_source = "",
                 anime_background = "",
                 anime_premiered = "",
                 anime_status = "",
                 anime_broadcast = "",
                 anime_producers = "",
                 anime_licensors = "",
                 anime_studios = "",
                 anime_duration = "",
                 anime_side_story = "",
                 anime_adaptation = "",
                 anime_summary = "",
                 anime_full_story = "",
                 anime_parent_story = "",
                 anime_sequel = "",
                 anime_prequel = "",
                 anime_alternative_setting = "",
                 anime_other = "",
                 anime_reviews = None):
        self.anime_index = anime_index
        self.anime_id = anime_id
        self.anime_english_title = anime_english_title
        self.anime_japanese_title = anime_japanese_title
        self.anime_image_url = anime_image_url
        if not anime_genres:
            anime_genres = []
        self.anime_genres = anime_genres
        self.anime_synopsis = anime_synopsis
        self.anime_rating_value = anime_rating_value
        self.anime_rating_count = anime_rating_count
        self.anime_rating = anime_rating
        self.anime_popularity = anime_popularity
        self.anime_favorites = anime_favorites
        self.anime_members = anime_members
        self.anime_number_of_episodes = anime_number_of_episodes
        self.anime_type = anime_type
        self.anime_source = anime_source
        self.anime_background = anime_background
        self.anime_premiered = anime_premiered
        self.anime_status = anime_status
        self.anime_broadcast = anime_broadcast
        self.anime_producers = anime_producers
        self.anime_licensors = anime_licensors
        self.anime_studios = anime_studios
        self.anime_duration = anime_duration
        self.anime_summary = anime_summary
        self.anime_full_story = anime_full_story
        self.anime_parent_story = anime_parent_story
        self.anime_sequel = anime_sequel
        self.anime_prequel = anime_prequel
        self.anime_alternative_setting = anime_alternative_setting
        self.anime_other = anime_other
        if not anime_reviews:
            anime_reviews = []
        self.anime_reviews = anime_reviews

    def addReview(self, review):
        if isinstance(review, Review):
            if not any(other.__dict__ == review.__dict__ for other in self.anime_reviews):
                self.anime_reviews.append(review)
            else:
                print("DUPLICATE DICT")
        else:
            raise ValueError("object is not instance of Review")

    def addGenre(self, genre):
        if genre not in self.anime_genres:
            self.anime_genres.append(genre)

    def getAllReviewText(self):
        return " ".join([review.review_text for review in self.anime_reviews])

    def toJSON(self):
        dictionaryRepresentation = self.__dict__
        dictionaryRepresentation['anime_reviews'] = [review.toJSON() for review in self.anime_reviews]
        return dictionaryRepresentation
