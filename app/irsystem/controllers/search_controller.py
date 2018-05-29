# -*- coding: utf-8 -*-
from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import numpy as np
import json
import operator
import gensim.models
import re
from scipy.sparse.linalg import svds
from flask import redirect
# from sklearn.preprocessing import normalize
# import html

project_name = "Aniai: Anime Recommender"
net_id = "Arthur Chen (ac2266), Henry Levine (hal59), Kelley Zhang (kz53), Gary Gao (gg392), Cheyenne Biolsi (ckb59)"

number_results = 200 #Number Results Before PostProcessing
number_results_final = 100
weight_tags = 1
weight_title = 6

allanimelite = json.load(open('app/static/data/anime_info.json'))
#for index, element in enumerate(allanimelite):
#	assert int(element["anime_index"]) == index

tags_data = np.load('data/tags.npy')
alltags_data = np.load('data/alltags.npy')

tags_column = tags_data[:,0]
tags_nocolumn = np.delete(tags_data, 0, 1)

alltags_column = alltags_data[:,0]
alltags_nocolumn = np.delete(alltags_data, 0, 1)

# Trucated SVD
#firstcolumn = np.load('data/firstcolumn.npy') #Deprecated with New data
# allfirst_column = np.load('data/allfirst_column')
# u = np.load('data/u_reviewk40.npy')
# s = np.load('data/s_reviewk40.npy')
# vT = np.load('data/vT_reviewk40.npy')

# doc2vec
# review_model = gensim.models.doc2vec.Doc2Vec.load("data/doc2vecreview.model")

# doc2vec numpy
review_array = np.load("data/doc2vecreviewArray2.npy")
filter_bools= np.load("data/filterArray.npy")
word_array=np.load("data/wordArray2.npy")
word_list=np.load("data/wordList2.npy")
rat_array=np.load("data/ratArray.npy")
word_to_ind=dict()
for index,word in enumerate(word_list):
	word_to_ind[word]=index

animeJsonFile = 'app/static/data/anime_info.json'
animeReviewVectorRepresentationsFile = "data/doc2vecreviewArray2.npy"
filterBoolsFile = "data/filterArray.npy"
wordListFile = "data/wordList2.npy"
wordRepresentationsFile = "data/wordArray2.npy"
animeRatingsFile = "data/ratArray.npy"

class DataManager:
    def __init__(self, animeJsonFile, animeReviewVectorRepresentationsFile, filterBoolsFile, 
                       wordListFile, wordRepresentationsFile, animeRatingsFile):
        with open(animeJsonFile, 'r') as jsonFile:
            self.animeJson = json.load(jsonFile)
        self.animeReviewVectors = np.load(animeReviewVectorRepresentationsFile)
        self.titleToIndexDictionary = {ele["anime_english_title"]: int(ele["anime_index"]) for ele in self.animeJson}
        self.filterBoolVectors = np.load(filterBoolsFile)
        self.wordList = np.load(wordListFile).flatten()
        self.wordReverseLookup = {word:index for index, word in enumerate(self.wordList)}
        self.wordVectors = np.load(wordRepresentationsFile)
        self.ratingsValues = np.load(animeRatingsFile).flatten()

    def getAnimeVectors(self, animeIndices):
        return np.take(self.animeReviewVectors, animeIndices, axis=0)

    def getAnimeIndices(self, animeTitles):
        if type(animeTitles) == str or type(animeTitles) == unicode:
            return self.titleToIndexDictionary[animeTitles]
        return np.asarray([self.titleToIndexDictionary[title] for title in animeTitles])

    def getAnimeJson(self, animeIndices):
        if isinstance(animeIndices, int):
            return self.animeJson[animeIndices]
        else:
            return [self.animeJson[index] for index in animeIndices]

    def getWordVectors(self, wordIndices):
        return np.take(self.wordVectors, wordIndices, axis=0)

    def getWords(self, wordIndices):
        return np.take(self.wordList, wordIndices)

    def getWordIndices(self, wordStrings):
        if type(wordStrings) == str or type(wordStrings) == unicode:
            return self.wordReverseLookup[wordStrings]
        return np.asarray([self.wordReverseLookup[word] for word in wordStrings])

    def getRatings(self, animeIndices):
        return np.take(self.ratingsValues, animeIndices)

animeJsonFile = 'app/static/data/anime_info.json'
animeReviewVectorRepresentationsFile = "data/doc2vecreviewArray2.npy"
filterBoolsFile = "data/filterArray.npy"
wordListFile = "data/wordList2.npy"
wordRepresentationsFile = "data/wordArray2.npy"
animeRatingsFile = "data/ratArray.npy"

dataManager = DataManager(animeJsonFile, animeReviewVectorRepresentationsFile,
                          filterBoolsFile, wordListFile, wordRepresentationsFile,
                          animeRatingsFile)
# Tags and Jaccard Similarity
FILTER_ORDER = ['action','adventure','cars','comedy','dementia','demons','mystery','drama','ecchi','fantasy','game','hentai','historical','horror','kids','magic','martial_arts','mecha','music','parody','samurai','romance','school','sci-fi','shoujo','shoujo-ai','shounen','shounen-ai','space','sports','super_power','vampire','yaoi','yuri','harem','slice_of_life','supernatural','military','police','psychological','thriller','seinen','josei','displayTv', 'displayMovie', 'displayOva', 'displayOna', 'displaySpecial','streamCrunchy', 'streamHulu', 'streamYahoo', 'streamNone',"gRating", "pgRating", "pg13Rating", "r17Rating","rPlusRating","rxRating",'filter same series']


import requests
@irsystem.route('/searchx', methods=['POST'])
def search2():
    print("IN TEST")
    print(request)
    r = requests.post(request.url_root + "search/animesearch=Naruto")
    return r 

@irsystem.route('/', methods=['GET'])
def index():
    return render_template('search.html', name=project_name, netid=net_id, output_message='', data=[], \
                           prevsearch=keep(None), prevwords=keep(None), prevhide_ss=None, prevtv=None, prevfilters2=None, filtertrue = False, sfw_on = True, original_value=[])



class FilterManager:
    def __init__(self, dataManager):
        self.dataManager = dataManager
        self.filterMapping = {val:index for index, val in enumerate(FILTER_ORDER)}

    def getHotEncodedFilterFromRequest(self, request):
        filterString = request.args.get('filters').decode('base64')
        filters = filterString.split('&')
        desiredAttributes = np.zeros((len(FILTER_ORDER)), dtype=bool)
        for attributeName in filters:
            if (attributeName in self.filterMapping):
                filterIndex = self.filterMapping[attributeName]
                desiredAttributes[filterIndex] = True
            else:
                print('Skipping filter: {}'.format(attributeName))
        return desiredAttributes

    def getFilterDictionaryFromRequest(self, request):
        filterString = request.args.get('filters').decode('base64')
        filters = filterString.split('&')
        filterDictionary = {}
        for attributeName in filters:
            filterDictionary[attributeName] = True
        for attributeName in FILTER_ORDER:
            if not attributeName in filterDictionary:
                filterDictionary[attributeName] = False
        return filterDictionary

    def getFilteredShowIndices(self, request, animeTitles):
        filterArray = self.getHotEncodedFilterFromRequest(request)
        matchingFilters = self.dataManager.filterBoolVectors[:, filterArray]
        removedShowIndices = np.where(matchingFilters.any(axis=1))[0]
        queryShows = np.asarray([title.index for title in animeTitles])
        return np.append(removedShowIndices, queryShows)

filterManager = FilterManager(dataManager)

class AnimeManager:
    def __init__(self, animeJsonFile):
        with open(animeJsonFile, 'r') as jsonFile:
            self.animeJson =  json.load(jsonFile)

class AnimeTitle:
    def __init__(self, index, sign):
        self.index = index
        self.sign = sign

class AnimeTitleFactory:
    def __init__(self, dataManager):
        self.dataManager = dataManager

    def buildAnimeTitles(self, request):
        animeStringTitles = set(request.args.get('animesearch').split('|'))
        animeTitles = []
        for title in animeStringTitles:
            if len(title) <= 0:
                continue
            if title[0] == "!":
                index = self.dataManager.getAnimeIndices(title[1:])
                animeTitles.append(AnimeTitle(index, False))
            else:
                index = self.dataManager.getAnimeIndices(title)
                animeTitles.append(AnimeTitle(index, True))
        return animeTitles

class AnimeRequestManager:
    def __init__(self, animeTitleFactory, dataManager):
        self.animeTitleFactory = animeTitleFactory
        self.dataManager = dataManager

    def getAnimeEncodings(self, animeTitles, sign=True):
        return np.asarray([title.index for title in animeTitles if title.sign == sign])

    def getAnimeQueryVectorizedRepresentation(self, request):
        animeTitles = self.animeTitleFactory.buildAnimeTitles(request)
        positiveAnimeIndices = self.getAnimeEncodings(animeTitles, sign=True)
        negativeAnimeIndices = self.getAnimeEncodings(animeTitles, sign=False)
        vectorizedRepresentation = np.zeros((self.dataManager.animeReviewVectors.shape[1]))
        if positiveAnimeIndices.shape[0]:
            positiveAnimeRepresentations = self.dataManager.animeReviewVectors[positiveAnimeIndices, :]
            vectorizedRepresentation = vectorizedRepresentation + np.sum(positiveAnimeRepresentations, axis=0)
        if negativeAnimeIndices.shape[0]:
            negativeAnimeRepresentations = self.dataManager.animeReviewVectors[negativeAnimeIndices, :]
            vectorizedRepresentation = vectorizedRepresentation - np.sum(negativeAnimeRepresentations, axis=0)
        return vectorizedRepresentation

animeManager = AnimeManager('app/static/data/anime_info.json')
animeTitleFactory = AnimeTitleFactory(dataManager)
animeRequestManager = AnimeRequestManager(animeTitleFactory, dataManager)

class Word:
    def __init__(self, index, word, sign):
        self.index = index
        self.word = word
        self.sign = sign

class WordFactory:
    def __init__(self, dataManager):
        self.dataManager = dataManager

    def buildWords(self, request):
        wordStrings = set(request.args.get('wordsearch').split('|'))
        words = []
        for word in wordStrings:
            if len(word) <= 0:
                continue
            if word[0] == "!":
                word = word[1:]
                index = self.dataManager.getWordIndices(word)
                words.append(Word(index, word, False))
            else:
                index = self.dataManager.getWordIndices(word)
                words.append(Word(index, word, True))
        return words 

class WordRequestManager:
    def __init__(self, wordFactory, dataManager):
        self.wordFactory = wordFactory
        self.dataManager = dataManager

    def getWordEncodings(self, words, sign=True):
        return np.asarray([word.index for word in words if word.sign == sign])

    def getWordQueryVectorizedRepresentation(self, request):
        words = self.wordFactory.buildWords(request)
        positiveWordIndices = self.getWordEncodings(words, sign=True)
        negativeWordIndices = self.getWordEncodings(words, sign=False)
        vectorizedRepresentation = np.zeros((self.dataManager.wordVectors.shape[1]))
        if positiveWordIndices.shape[0]:
            positiveWordRepresentations = self.dataManager.wordVectors[positiveWordIndices, :]
            vectorizedRepresentation += np.sum(positiveWordRepresentations, axis=0)
        if negativeWordIndices.shape[0]:
            negativeWordRepresentations = self.dataManager.wordVectors[negativeWordIndices, :]
            vectorizedRepresentation -= np.sum(negativeWordRepresentations, axis=0)
        return vectorizedRepresentation

wordFactory = WordFactory(dataManager)
wordRequestManager = WordRequestManager(wordFactory, dataManager)

class SuggestionFactory:
    def __init__(self, dataManager, animeRequestManager, wordRequestManager, ratingsDataFile):
        self.dataManager = dataManager
        self.animeRequestManager = animeRequestManager
        self.wordRequestManager = wordRequestManager
        self.ratingsData = np.load(ratingsDataFile)

    def buildSuggestions(self, animeQueryRepresentation, wordQueryRepresentation, filteredShowIndices, numSuggestions = 20):
        vectorizedQuery = wordQueryRepresentation + animeQueryRepresentation
        suggestedIndices, animeScores = self.buildSuggestedIndices(vectorizedQuery, filteredShowIndices, numSuggestions)
        jsonList = []
        for index in range(len(suggestedIndices)):
            if len(jsonList) == numSuggestions:
                return jsonList
            jsonList.append(self.buildSuggestion(suggestedIndices[index], vectorizedQuery, animeScores[index]))
        return jsonList

    def buildSuggestedIndices(self, vectorizedQuery, filteredShowIndices, numSuggestions):
	scores=self.cossim(self.dataManager.animeReviewVectors,vectorizedQuery)
        adjustedScores = scores.flatten("F") + (0.1)*self.ratingsData
        suggestionIndices = np.argsort(-adjustedScores, axis=0)
        mask = np.isin(suggestionIndices, filteredShowIndices, invert=True)
        filteredSuggestionIndices = suggestionIndices[mask][:numSuggestions].flatten()
        return filteredSuggestionIndices, np.take(adjustedScores, filteredSuggestionIndices).flatten()

    def topRelatedWords(self, query, number = 10):
        similarities = self.cossim(self.dataManager.wordVectors, query).flatten()
        topIndices = np.argsort(-similarities)[:number]
        topScores = np.take(similarities, topIndices)
        topWords = self.dataManager.getWords(topIndices)
        return zip(topWords, topIndices, topScores)

    def cossim(self, vectorized, query):
        query = query.flatten()
        if vectorized.ndim == 1:
            return np.matmul(vectorized,query)/(np.linalg.norm(vectorized) * np.linalg.norm(query))
        return np.matmul(vectorized, query)/(np.linalg.norm(vectorized, axis=1) * np.linalg.norm(query))

    def getTopWordsInCommon(self, query, animeVectorRepresentation, number=10): 
        queryToWordsSim = self.cossim(self.dataManager.wordVectors, query)
        animeToWordsSim = self.cossim(self.dataManager.wordVectors, animeVectorRepresentation)
        similarities = (queryToWordsSim * animeToWordsSim) / (np.linalg.norm(queryToWordsSim) * np.linalg.norm(animeToWordsSim))
        topIndicesInCommon = np.argsort(-similarities)[:3*number]
        topScoresInCommon = np.take(similarities, topIndicesInCommon)
        topWordsInCommon = self.dataManager.getWords(topIndicesInCommon)
        queryVals = np.take(queryToWordsSim, topIndicesInCommon)
        animeVals = np.take(animeToWordsSim, topIndicesInCommon)
        positiveIndices = (queryVals > 0) * (animeVals > 0)
        topWordsInCommon = topWordsInCommon[positiveIndices][:number]
        queryScoresInCommon = queryVals[positiveIndices][:number]
        animeScoresInCommon = animeVals[positiveIndices][:number]
        return zip(topWordsInCommon, queryScoresInCommon, animeScoresInCommon)
        
    def buildSuggestion(self, animeIndex, query, score):
        animeJson = self.dataManager.getAnimeJson(animeIndex)
	animeVectorRepresentation=self.dataManager.getAnimeVectors(animeIndex)
        topWordTagsForAnime = zip(*self.topRelatedWords(animeVectorRepresentation))[0]
        topWordsInCommon, queryScoresInCommon, animeScoresInCommon = zip(*self.getTopWordsInCommon(query, animeVectorRepresentation, 10))
        animeJson['words'] = "|".join(topWordTagsForAnime)
        animeJson['graph_words'] = "|".join(topWordsInCommon)
        animeJson['graph_value'] = list(np.round(queryScoresInCommon, 3))
        animeJson['original_value'] = list(np.round(animeScoresInCommon, 3))
        animeJson['score'] = str(round(score*100, 2))
        return animeJson
    
suggestionFactory = SuggestionFactory(dataManager, animeRequestManager, wordRequestManager, "data/ratArray.npy")

@irsystem.route('/search', methods=['GET'])
def search():
        animeTitles = animeTitleFactory.buildAnimeTitles(request)
        filteredShowIndices = filterManager.getFilteredShowIndices(request, animeTitles)
        filterDictionary = filterManager.getFilterDictionaryFromRequest(request)
        animeQueryRepresentation = animeRequestManager.getAnimeQueryVectorizedRepresentation(request)
        wordQueryRepresentation = wordRequestManager.getWordQueryVectorizedRepresentation(request)
        data = suggestionFactory.buildSuggestions(animeQueryRepresentation, wordQueryRepresentation, filteredShowIndices)

	query = request.args.get('animesearch')
	words = request.args.get('wordsearch')
        print("query: {}".format(query))
	filtered_true = False
        shows_removed = filteredShowIndices
	if query or words: 
		filtered_true = True
        sfw_on = request.args.get('sfw') == "on"
	filter_out=np.zeros((len(FILTER_ORDER)),dtype=bool)
	filter_dictionary2=dict()
	for index, filters in enumerate(FILTER_ORDER):
		switch=request.args.get(filters)
		filter_dictionary2[filters] = switch
	# Option 1: No Anime or Tags
        filter_dictionary2 = filterDictionary
	if not query and not words:
		data = []
		output_message = ''
		originalValue = []
	# Option 3: Only Anime
	else:
		anime_names = query.split('|')
		anime_set=set(anime_names)
		pos_id_set, neg_id_set =get_anime_set_pn(anime_set,allanimelite) 
		query_words = words.split('|')
                pos_query_words = [word for word in query_words if len(word) > 0 and word[0] != "!"]
                neg_query_words = [word[1:] for word in query_words if len(word) > 0 and word[0] == "!"]
		output_message = ''
                
		if(not query=='None'):
			positive = np.zeros((len(pos_id_set)),dtype=int)
			for index,anim_ind in enumerate(pos_id_set):
				positive[index]=int(anim_ind)
			negative = np.zeros((len(neg_id_set)),dtype=int)
			for index,anim_ind in enumerate(neg_id_set):
				negative[index]=int(anim_ind)
		else:
			positive= np.zeros((0))
                        negative = np.zeros((0))
			set_anime_ids=set()
	
		if(not words=='None'):
			positive_words=np.zeros((len(pos_query_words)),dtype=int)
			for index,word in enumerate(pos_query_words):
				positive_words[index]=word_to_ind.get(word,-1)
			positive_words=positive_words[positive_words>=0]
                        negative_words = np.zeros((len(neg_query_words)),dtype=int)
                        for index, word in enumerate(neg_query_words):
                                negative_words[index]=word_to_ind.get(word, -1)
                        negative_words = negative_words[negative_words>=0]
		else:
                        negative_words = np.zeros((0))
			positive_words= np.zeros((0))

 
		show_result=np.zeros((review_array.shape[1]))
		if(len(positive)>0):
			positive_show_vectors = review_array[positive,:]
			show_result=np.sum(positive_show_vectors,axis=0)
                if(len(negative)>0):
                        negative_show_vectors = review_array[negative,:]
                        negative_show_result = np.sum(negative_show_vectors, axis=0)
                        show_result = show_result - negative_show_result 

		word_result=np.zeros((review_array.shape[1]))
		if(len(positive_words)>0):           
			positive_word_vectors = word_array[positive_words,:]
			word_result=np.sum(positive_word_vectors,axis=0)
                if(len(negative_words)>0):
                        negative_word_vectors = word_array[negative_words,:]
                        word_result = word_result - np.sum(negative_word_vectors, axis=0)
                print("Equal: {}".format(show_result - animeQueryRepresentation))
		result=show_result+word_result    
                result = wordQueryRepresentation + animeQueryRepresentation
		result=result/np.linalg.norm(result)       
		scores=np.matmul((review_array),(result[:,np.newaxis]))
		word_scores=np.matmul((word_array),(result[:,np.newaxis]))
		adjust=scores.flatten("F")+(.1)*rat_array
		top_shows_unfiltered= np.argsort(-adjust,axis=0)
		top_words= np.argsort(-word_scores,axis=0)
        
            #filter out the shows we don't want
		mask=np.isin(top_shows_unfiltered,shows_removed,invert=True)
		print(np.where(mask==False))
		top_shows=top_shows_unfiltered[mask]   
		top_n_shows= top_shows[:20]

		bottom_n_shows= top_shows[-20:]
		if(len(top_n_shows)<=0):
			output_message = "Impossible Combination. Please Change Filters."
			return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=[], 
				prevsearch=keep(query), prevwords=keep(words), prevhide_ss=not(filter_out[-1]), prevtv=filter_out[43], prevfilters2=filter_dictionary2, filtertrue = filtered_true, sfw_on = sfw_on, original_value=[])


            
# 		norm=scores[top_shows[0]]
# 		if(norm==1):
# 			norm=scores[top_shows[1]]    
# 		scores=scores/np.max(norm)
 		# rocchio
  		weights=weights=1/(np.arange(20.).reshape((20,1))+1)  
  		for value in enumerate(positive):
  			anim_id=value[1]
  			rocchiod=rocchio(review_array[anim_id], review_array[top_n_shows]*weights,         review_array[bottom_n_shows]*weights,a=.3, b=.3*float(1)/len(positive), c=.3*float(1)/len(positive))
  			review_array[anim_id]=rocchiod/np.linalg.norm(rocchiod)
  			print(np.linalg.norm(rocchiod/np.linalg.norm(rocchiod)-result))
   		for value in enumerate(positive_words):
   			word_id=value[1]
   			rocchiod=rocchio(word_array[word_id], review_array[top_n_shows]*weights,         review_array[bottom_n_shows]*weights, a=1, b=3*float(1)/len(positive_words), c=3*float(1)/len(positive_words)) 
   			word_array[word_id]=rocchiod/np.linalg.norm(rocchiod)

		top_n_words=top_words[:10]
        
        
		json_array = []      
#                top_n_shows = suggestedIndices 
            #returns most similar anime ids and similarity scores
		for anim_ind in []:
			score = adjust[anim_ind]
			jsonfile = get_anime(anim_ind, allanimelite)
			wordvec = get_top_words(anim_ind)   
			concat="|".join(wordvec)                
			if anim_ind not in pos_id_set and anim_ind not in neg_id_set and jsonfile != "not found":
				jsonfile['score'] =str(round(score*100, 2))
				show_word_result=np.matmul(word_array,review_array[anim_ind])
				new_results=show_word_result+word_scores.flatten('F')
				new_top_words=np.argsort(-new_results,axis=0)
				new_top_n_words=new_top_words[:10]
				new_top_word_vecs=word_array[new_top_n_words]
				jsonfile['words'] = concat
				jsonfile['graph_words']="|".join(word_list[new_top_n_words.flatten('F')])
				newscores=np.matmul(new_top_word_vecs,review_array[anim_ind])
				newscores=np.round(newscores.flatten('F'),3)
				neworigscore=np.matmul(new_top_word_vecs,result)
				neworigscore=np.round(neworigscore.flatten('F'),3)
				jsonfile['graph_value']=list(newscores)
				jsonfile['original_value']=list(neworigscore)

				json_array.append(jsonfile)

		#newwordscores=np.matmul(top_words_vecs,result)
		#wordflatscores=np.round(newwordscores.flatten('F'),3)
		#originalValue=list(wordflatscores)

#		data = json_array
	# print(data)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, 
		prevsearch=keep(query), prevwords=keep(words), prevhide_ss=not(filter_out[-1]), prevtv=filter_out[43], prevfilters2=filter_dictionary2, filtertrue = filtered_true, sfw_on = sfw_on, original_value=[])

# def fake_most_similiar(positive, negative, matrix, topn) {
# 	for pos in positive:

# }

def get_top_words(anime_index,howmany=10):
	query=review_array[anime_index]
	scores=np.matmul((word_array),(query.T))
	top_words_ind= np.argsort(-scores,axis=0)
	top_n_words_ind = top_words_ind[:howmany]
	top_n_words=word_list[top_n_words_ind]
	return top_n_words.flatten(order="F")

def get_anime_set(anime_set, jsonfile):
	# print(anime_id)
	id_set=set()    
	for element in jsonfile:
		# print(element['anime_id'])
		name=(element["anime_english_title"])
		if (element["anime_english_title"] in anime_set):
			id_set.add(int(element['anime_index']))
			anime_set.remove(element['anime_english_title'])
			if(len(anime_set)==0):
				break
	return id_set

def get_anime_set_pn(anime_set, jsonfile):
    dictionary = {ele["anime_english_title"]: ele["anime_index"] for ele in jsonfile}
    positive_ids = set()
    negative_ids = set()
    for title in anime_set:
        if len(title) <= 0:
            continue
        if title[0] == "!":
            negative_ids.add(int((dictionary[title[1:]])))
        else:
            positive_ids.add(int(dictionary[title]))
    return positive_ids, negative_ids

def get_anime(anime_index, jsonfile):
	# print(anime_id)
	for element in jsonfile:
		# print(element['anime_id'])
		if (element['anime_index']) == anime_index:
			return element
	return "not found"

def get_cossim(queryvector, ind2, tfidf):
	"""Returns a float giving the cosine similarity of 
	   the two anime's npy (either based on reviews/reviews and synopsis/synopsis.
	
	Params: {mov1: String,
			 mov2: String,
			 input_doc_mat: Numpy Array,
			 movie_name_to_index: Dict}
	Returns: Float (Cosine similarity of the two movie transcripts.)
	"""
	# YOUR CODE HERE
	# numpy matrix whose shape is the number of documents by the number of words you're considering max 5000
	othervector = tfidf[ind2,:]
	numerator = np.dot(queryvector, othervector)
	denominator = (np.dot(np.linalg.norm(queryvector), np.linalg.norm(othervector)))
	return numerator/denominator

def get_jaccard(setA, setB):
	if len(setB) != 0:
		jacsim = float(len(setA & setB))/float(len(setA | setB))
		return jacsim
	else:
		return 0.0

def hide_sameseries(anime_ids, data, jsonfile):
	hide = []
	for anime_id in anime_ids:
		anime = get_anime(anime_id, jsonfile)

		if anime["anime_side_story"] != "":
			sidestory = anime["anime_side_story"]
			sidestory_anime = re.findall('\((.*?)\)',sidestory)
			if sidestory != []:
				for ss in sidestory_anime:
					hide.append(int(ss.replace('anime ','')))
		
		if anime["anime_parent_story"] != "":
			parentstory = anime["anime_parent_story"]
			# print('parent',parentstory)
			parentstory = re.findall('\((.*?)\)',parentstory)

			if parentstory != []:
				for ps in parentstory:
					pstory = ps.replace('anime ','')
					# print(pstory, 'pstory')
					if int(pstory) not in hide:
						print('yes')
						pstory_anime = get_anime(int(pstory), jsonfile)
						print(pstory_anime)
						if pstory_anime != "not found":
							hide.append(int(pstory))
							if pstory_anime["anime_side_story"] != "":
								sidestory2 = pstory_anime["anime_side_story"]
								sidestory_anime2 = re.findall('\((.*?)\)',sidestory2)
								if sidestory2 != []:
									for ss2 in sidestory_anime2:
										hide.append(int(ss2.replace('anime ','')))

	hide_set = set(hide)
	new_data = []
	for entry in data:
		if entry != "not found":
			if entry['anime_index'] not in hide_set:
				new_data.append(entry)

	return new_data

def hide_filter(data, jsonfile, show, min_rating, time, finished, licensed, age, genre, activestream, sfw):
	# Filters: TV, Movie, OVA, Special, OVA, Minimum Anime Rating, Time Period
	new_data = []
	print('show', show)
	print('age', age)
	print('genre', genre)
	print('activestream', activestream)
	# print('1',age)
	# print('2',len(age))
	# print('3',genre)
	# print('4',len(genre))
	for entry in data:
		if entry != "not found":

			min_rating_add = True
			if min_rating: 
				if entry['anime_rating_value'] != "":
					if float(entry['anime_rating_value']) < float(min_rating):
						min_rating_add = False
				else:
					min_rating_add = False

			time_add = True
			if time:
				if entry['anime_premiered'] != 'N/A':
					year = re.findall('\d', entry['anime_premiered'])
					year = ''.join(year)
					if year < int(time):
						time_add = False
				else:
					time_add = False	

			finished_add = True
			if finished:
				if entry['anime_status'] != "Finished Airing" and entry['anime_status'] != "":
					finished_add = False

			show_add = True
			if show:
				if entry['anime_type'] not in show:
					# TV, Movie, OVA, Special, OVA 
					show_add = False

			licensed_add = True
			if licensed:
				if entry['anime_licensors'] == "":
					licensed_add = False

			# Doesn't work
			age_add = True
			# print('1',age)
			# print('2',len(age))
			if len(age) > 0:
				if entry['anime_rating'] not in age:
					age_add = False

			genre_add = False #no genres no results
			if len(genre) > 0:
				genres = re.findall("[a-zA-z]*", entry['anime_genres'])
				anime_genres = [x.lower() for x in genres]
				for anime_genre in anime_genres:
					if anime_genre in genre:
						genre_add = True


			# Doesn't work
			stream_add = True
			# if len(activestream) > 0:
			# 	if entry['ac']

			sfw_add = True
			if not sfw:
				if entry['anime_rating'] in set(["R+ - Mild Nudity", "Rx - hentai"]):
					sfw_add = False

			if min_rating_add and time_add and finished_add and show_add and licensed_add and age_add and genre_add and stream_add and sfw_add:
				new_data.append(entry)

	return new_data

def rocchio(query, relevant, irrelevant,a=.3, b=.3, c=.8, clip = False):
	q0 = query
	if relevant.shape[0]!=0 and irrelevant.shape[0]!=0:
		q1 = (a*q0)+(b*(1/relevant.shape[0])*np.sum(relevant,axis=0))-(c*((1/irrelevant.shape[0])*np.sum(irrelevant,axis=0)))
	if clip:
		q1[q1<0] = 0

	return q1

def makeListsOfList(data_list):
	return [data_list[i:i+8] for i in range(0, len(data_list), 8)]

def keep(x):
	if x == None:
		return ""
	else:
		return x

