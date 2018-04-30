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
# from sklearn.preprocessing import normalize
# import html

project_name = "Aniai: Anime Recommender"
net_id = "Arthur Chen (ac2266), Henry Levine (hal59), Kelley Zhang (kz53), Gary Gao (gg392), Cheyenne Biolsi (ckb59)"

number_results = 200 #Number Results Before PostProcessing
number_results_final = 100
weight_tags = 1
weight_title = 6

allanimelite = json.load(open('app/static/data/anime_search.json'))
for index, element in enumerate(allanimelite):
    element["anime_index"] = index

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
review_array = np.load("data/doc2vecreviewArray.npy")
word_array=np.load("data/wordArray.npy")
words=np.load("data/wordList.npy")
word_to_ind=dict()
for index,word in enumerate(words):
    word_to_ind[word]=index


# Tags and Jaccard Similarity
tags_array = ['action','adventure','cars','comedy','dementia','demons','mystery','drama','ecchi','fantasy','game','hentai','historical','horror','kids','magic','martial_arts','mecha','music','parody','samurai','romance','school','sci-fi','shoujo','shoujo_ai','shounen','shounen_ai','space','sports','super_power','vampire','yaoi','yuri','harem','slice_of_life','supernatural','military','police','psychological','thriller','seinen','josei']
ty_pe = ['displayTv', 'displayMovie', 'displayOva', 'ona', 'displaySpecial']
tags_set = set(tags_array)

@irsystem.route('/', methods=['GET'])

def search():
	query = request.args.get('animesearch')
	tag = request.args.get('tagsearch')

	#hide same series filter
	hide_ss = request.args.get('filter same series')
	
	# TV Filter
	type_dictionary = {}
	for meep in ty_pe:
		print('meep',request.args.get(meep))
		type_dictionary[meep] = request.args.get(meep)

	tv = request.args.get('displayTv')
	# print(tv)
	movie = request.args.get('displayMovie')
	ova = request.args.get('displayOva')
	ona = request.args.get('displayOna')
	special = request.args.get('displaySpecial')
	
	show = []
	if tv:
		show.append('TV')
	if movie:
		show.append('Movie')
	if ova:
		show.append('OVA')
	if ona:
		show.append('ONA')
	if special:
		show.append('Special')

	set_show = set(show)

	# Genre Filter
	tags_dictionary = {}
	for tagz in tags_array:
		tags_dictionary[tagz] = request.args.get(tagz)

	activegenre = []
	for key, value in tags_dictionary.iteritems():
		if value != None:
			activegenre.append(key)

	set_activegenre = set(activegenre)

	# Age Rating Filter
	guidance_dictionary = {}
	for guidance_rating in ["gRating", "pgRating", "pg13Rating", "r17Rating","rPlusRating","rxRating"]:
		if guidance_rating == "gRating":
			guidance_dictionary["G - All Ages"] = request.args.get(guidance_rating)
		elif guidance_rating == "pg13Rating":
			guidance_dictionary["PG-13 - Teens 13 or older"] = request.args.get(guidance_rating)
		elif guidance_rating == "pgRating":
			guidance_dictionary["PG - Children"] = request.args.get(guidance_rating)
		elif guidance_rating == "r17Rating":
			guidance_dictionary["R - 17+ (violence & profanity)"] = request.args.get(guidance_rating)
		elif guidance_rating == "rPlusRating":
			guidance_dictionary["R+ - Mild Nudity"] = request.args.get(guidance_rating)
		elif guidance_rating == "rxRating":
			guidance_dictionary["Rx — hentai"] = request.args.get(guidance_rating)
		# "R+ - Mild Nudity"
		# Rx

	active_guidance = []
	for key, value in guidance_dictionary.iteritems():
		if value != None:
			active_guidance.append(key)

	set_guidance = set(active_guidance)

	# Stream Filter
	stream_dictionary = {}
	for stream in ["streamCrunchy", "streamHulu", "streamYahoo", "streamNone"]:
		stream_dictionary[stream] = request.args.get(stream)


	# FIX
	activestream = []
	for key, value in stream_dictionary.iteritems():
		if value != None:
			activestream.append(key)

	set_stream = set(activestream)  

	#NSFW fitler
	sfw = request.args.get('sfw')

	# Min Rating Filter
	min_rating = request.args.get('min_rating')

	# Time Filter
	time = request.args.get('time')

	# Finished Filter
	finished = request.args.get('finished')

	# Licensed Filter
	licensed = request.args.get('licensed')




	# Option 1: No Anime or Tags
	if not query and not tag:
		data = []
		output_message = ''
	# Option 3: Only Anime
	else:
		anime_indexes = query.split('|')
		#query_words = tag.split('|')

		if -1 in anime_indexes:
			data = []
			output_message = 'Could not find your show. Please try again.'
		else:
			output_message = 'Your search: ' + query
            
			positive = np.zeros((len(anime_indexes)),dtype=int)
			for index,anim_ind in enumerate(anime_indexes):
				positive[index]=int(anim_ind)
			set_anime_ids=set(positive)
			print(positive)
            
# 			positive_words=np.zeros((len(query_words)))
# 			for index,word in enumerate(quer_words):
# 				positive_words[index]=word_to_ind.get(word,-1)
# 			positive_words=positivewords[positive_words>=0]             

			positive_show_vectors = review_array[positive,:]
			show_result=np.sum(positive_show_vectors,axis=0)
            
           
# 			positive_word_vectors = review_array[positive_words,:]
# 			word_result=np.sum(positive_word_vectors,axis=0)
 			result=show_result#+word_result           

			scores=np.matmul((review_array),(result[:,np.newaxis]))
			top_shows= np.argsort(-scores,axis=0)
			top_n_shows= top_shows[:20]
			bottom_n_shows= top_shows[-20:]

			# rocchio
			for anim_id in enumerate(positive):
				review_array[anim_id]=rocchio(review_array[anim_id], top_n_shows, bottom_n_shows,
                                              a=.3, b=.3*float(1)/len(positive), c=.3*float(1)/len(positive))          
# 			for word_id in enumerate(positive_words):               
# 				review_array[anim_id]=rocchio(word_array[word_id], top_n_shows, bottom_n_shows,
#                                               a=.3, b=.3*float(1)/len(positive_words), c=.3*float(1)/len(positive_words))              
			json_array = []
            #returns most similar anime ids and similarity scores
			for array_ind, anim_ind in enumerate(top_n_shows):
				score = scores[array_ind]
				jsonfile = get_anime(anim_ind, allanimelite)
				wordvec = get_top_words(anim_ind)   
				concat="|".join(wordvec)                
				if anim_ind[0] not in set_anime_ids and jsonfile != "not found":
					jsonfile['score'] = score
					jsonfile['words'] = concat                    
					json_array.append(jsonfile)
			data = json_array
	# if Further Filters are chosen
	if hide_ss and query:
		data = hide_sameseries(anime_indexes, data, allanimelite)

	# if show or min_rating or time or finished or licensed or len(set_guidance) > 0 or len(set_activegenre) > 0 or len(set_stream) > 0 or sfw:
	data = hide_filter(data, allanimelite, set_show, min_rating, time, finished, licensed, set_guidance, set_activegenre, set_stream, sfw)

	# print(data)
	data = makeListsOfList(data)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, 
		prevsearch=query, prevtags=tag, prevhide_ss=hide_ss, prevtv=tv)

# def fake_most_similiar(positive, negative, matrix, topn) {
# 	for pos in positive:

# 		get_cossim()

	
# }

def get_top_words(anime_index,howmany=10):
    query=review_array[anime_index]
    scores=np.matmul((word_array),(query.T))
    top_words_ind= np.argsort(-scores,axis=0)
    top_n_words_ind = top_words_ind[:howmany]
    top_n_words=words[top_n_words_ind]
    return top_n_words.flatten(order="F")


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
    if relevant.shape[0]!=0:
        f = lambda i: np.array(relevant)[i]
        dREL = np.fromfunction(np.vectorize(f), (len(relevant),) , dtype=int)
        dREL = np.sum(dREL,axis=0)
    else:
        dREL = 0
      
    if irrelevant.shape[0]!=0:
        f = lambda i: np.array(irrelevant)[i]
        dNREL = np.fromfunction(np.vectorize(f), (len(irrelevant),) , dtype=int)
        dNREL = np.sum(dNREL,axis=0)
    else:
        dNREL = 0    
    
    if relevant.shape[0]!=0 and irrelevant.shape[0]!=0:
        q1 = (a*q0)+(b*(1/relevant.shape[0])*dREL)-(c*((1/irrelevant.shape[0])*dNREL))
    elif len(relevant)==0:
        q1 = (a*q0)-(c*((1/irrelevant.shape[0])*dNREL))
    elif len(irrelevant)==0:
        q1 = (a*q0)+(b*(1/relevant.shape[0])*dREL)

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

