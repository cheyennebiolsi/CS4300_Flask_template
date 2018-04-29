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

allanimelite = json.load(open('data/allanimelite.json'))
for index, element in enumerate(allanimelite):
    element["anime_index"] = index

tags_data = np.load('data/tags.npy')
alltags_data = np.load('data/alltags.npy')

tags_column = tags_data[:,0]
tags_nocolumn = np.delete(tags_data, 0, 1)

alltags_column = alltags_data[:,0]
alltags_nocolumn = np.delete(alltags_data, 0, 1)

# Trucated SVD
firstcolumn = np.load('data/firstcolumn.npy') #Deprecated with New data
# allfirst_column = np.load('data/allfirst_column')
# u = np.load('data/u_reviewk40.npy')
# s = np.load('data/s_reviewk40.npy')
# vT = np.load('data/vT_reviewk40.npy')

# dov2vec
review_model = gensim.models.doc2vec.Doc2Vec.load("data/doc2vecreview.model")


# Tags and Jaccard Similarity
tags_array = ['action','adventure','cars','comedy','dementia','demons','mystery','drama','ecchi','fantasy','game','hentai','historical','horror','kids','magic','martial_arts','mecha','music','parody','samurai','romance','school','sci-fi','shoujo','shoujo_ai','shounen','shounen_ai','space','sports','super_power','vampire','yaoi','yuri','harem','slice_of_life','supernatural','military','police','psychological','thriller','seinen','josei']
tags_set = set(tags_array)

@irsystem.route('/', methods=['GET'])

def search():
	query = request.args.get('animesearch')
	tag = request.args.get('tagsearch')
	hide_ss = request.args.get('hide_ss')
	
	# TV Filter
	tv = request.args.get('TV')
	movie = request.args.get('movie')
	ova = request.args.get('ova')
	ona = request.args.get('ona')
	special = request.args.get('special')
	method = request.args.get('method')

	# Genre Filter
	action = 'action', 'adventure', 'cars', 'comedy', 'dementia', 'demons', 'drama','fantasy', 'game', 'harem', 'historical', 'horror', 'josei', 'kids', 'magic', 'martial arts', 'meccha', 'military', 'music', 'mystery', 'parody', 'police', 'psychological', 'romance', 'samurai', 'school', 'sci-fi', 'seinen', 'shoujo', 'shoujo-ai', 'shounen', 'shounen-ai', 'slice of life', 'space', 'sports', 'super power', 'supernatural', 'thriller', 'vampire'
	
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

	min_rating = request.args.get('min_rating')
	time = request.args.get('time')
	finished = request.args.get('finished')
	licensed = request.args.get('licensed')

	# Option 1: No Anime or Tags
	if not query and not tag:
		data = []
		output_message = ''
	# Option 2: Only Tags
	elif not query and tag:
		tag_array = tag.split('|')
		tag_indexes = []
		for tag_input in tag_array:
			tag_index = -1
			for element in tags_set:
				if element == tag_input:
					tag_index = tags_array.index(tag_input)
			tag_indexes.append(tag_index)

		if -1 in tag_indexes:
			data = []
			output_message = 'Tag(s) ' + tag + ' do not exist. Pls try again.'
		else:
			output_message = 'You looked for the Tag(s) ' + tag
			mytag_set = set(tag_indexes)

			jaccsim = {}
			for i in range(alltags_column.size):
				anime_i_help = np.where(alltags_nocolumn[i,:] > 0) #PROBLEM!!
				anime_i_tags = anime_i_help[0]
				anime_i_set = set(anime_i_tags)
				# if alltags_column[i] == 28647:
				# 	print(np.where(alltags_data[i,:] > 0))
				# 	print(anime_i_help)
				jaccsim[alltags_column[i]] = round(get_jaccard(mytag_set, anime_i_set),4)
			# now it's be anime id

			sorted_results = sorted(jaccsim.items(), key=operator.itemgetter(1), reverse=True)
			topanimes = [i[0] for i in sorted_results] # returns key in order as 1D array
			# print(topanimes)
			top_n_animes = topanimes[:number_results] # these are by anime id
			
			json_array = []
			for ind in top_n_animes: #ind is row index not anime id
				jsonfile = get_anime(ind, allanimelite)
				if jsonfile != "not found":
					score = jaccsim[ind] #get score from diction
					jsonfile['score'] = score
					json_array.append(jsonfile)

			data = json_array

	# Option 3: Only Anime
	elif not tag and query:
		query_array = query.split('|')
		print(query_array)
		anime_indexes = []
		for anime_input in query_array:
			anime_index = -1
			for element in allanimelite:
				if element['anime_english_title'] == anime_input:
					anime_index = element['anime_id']
			anime_indexes.append(anime_index)
		print(anime_indexes)
		set_anime_ids = set(anime_indexes)

		if -1 in anime_indexes:
			data = []
			output_message = 'Could not find ' + query + '. Please try again pls.'
		else:
			output_message = 'Your search: ' + query

			positive = []
			for ind in anime_indexes:
				positive.append("anime_id_" + str(ind))

			print('Postive', positive)

			positive_vectors = []
			for anime_id in positive:
				reviewvector = review_model.docvecs[anime_id] #get vector by MAL id
				positive_vectors.append(reviewvector)

			# print('postive vectors', positive_vectors)
			top_n_animes = review_model.docvecs.most_similar(positive=positive_vectors, negative=[], topn=number_results) 
			#returns most similar anime ids and similarity scores
			# print(top_n_animes)

			json_array = []
			score_array = []
			for result in top_n_animes:
				get_anime_id = int(result[0].replace("anime_id_", ""))
				score = result[1]
				jsonfile = get_anime(get_anime_id, allanimelite)
				print(jsonfile)
				if get_anime_id not in set_anime_ids and jsonfile != "not found":
					jsonfile['score'] = score
					json_array.append(jsonfile)
					
			data = json_array
			print('help', data)

	# Option 4: Anime and Tags
	else: # Tag and Anime Still Needs Work
		
		query_array = query.split('|')
		anime_indexes = []
		for anime_input in query_array:
			anime_index = -1
			for element in allanimelite:
				if element['anime_english_title'] == anime_input:
					anime_index = element['anime_id']
			anime_indexes.append(anime_index)
			 
		set_anime_ids = set(anime_indexes)

		tag_array = tag.split('|')
		tag_indexes = []
		for tag_input in tag_array:
			tag_index = -1
			for element in tags_set:
				if element == tag_input:
					tag_index = tags_array.index(tag_input)
			tag_indexes.append(tag_index)

		if (-1 in tag_indexes) and (-1 in anime_indexes):
			data = []
			output_message = 'Wrong Tag(s) and Anime.'

		elif -1 in anime_indexes:
			data = []
			output_message = 'Wrong Anime'
		
		elif -1 in tag_indexes:
			data = []
			output_message = 'Tag(s) ' + tag + ' do not exist. Pls try again.'

		else:
			output_message = 'Your search: ' + query

			positive = []
			for ind in anime_indexes:
				positive.append("anime_id_" + str(ind))

			positive_vectors = []
			for anime_id in positive:
				reviewvector = review_model.docvecs[anime_id] #get vector by MAL id
				positive_vectors.append(reviewvector)

			top_n_animes = review_model.docvecs.most_similar(positive=positive_vectors, negative=[], topn=(alltags_column.size+1)) 
			#returns most similar anime ids and similarity scores

			cossim = {} #Cosine Score
			for result in top_n_animes:
				get_anime_id = int(result[0].replace("anime_id_", ""))
				score = result[1]
				cossim[get_anime_id] = score

			# print(cossim)
			top_n_animes_set = set(top_n_animes)
			# TAGS
			mytag_set = set(tag_indexes)
			jaccsim = {}
			for i in range(alltags_column.size):
				# if "anime_id_" + str(int(i)) in top_n_animes_set:
				if "anime_id_" + str(int(alltags_column[i])) in top_n_animes_set:
					anime_i_help = np.where(alltags_nocolumn[i,:] > 0) #PROBLEM!!
					anime_i_tags = anime_i_help[0]
					anime_i_set = set(anime_i_tags)
					print(anime_i_set)
					print('weksakskdaka',get_jaccard((mytag_set, anime_i_set),4))
					# print('merp',alltags_column[i])
					jaccsim[alltags_column[i]] = round(get_jaccard(mytag_set, anime_i_set),4)
				#jaccsim is always returning 0?
			# print('wtfsfassafafs',jaccsim)
			# now it's be anime id

			total = {}
			print('JEJFJFSJ')
			print('COSSIM',cossim[8]) #COSSIM is missing but it's in the json
			print('assfajsfjajafsja')
			# print('JACCSIM', jaccsim[8])
			for element in alltags_column: #animeid
				if "anime_id_" + str(int(element)) in top_n_animes_set:
				## THIS NEEDS TO BE FIXED  ##
				## JDSJDJSJDSJSDJSDJSKDDKS ##
				# if get_anime(element, allanimelite) != "not found":
					total_score = weight_title * cossim[element] + weight_tags * jaccsim[element]
					total[element] = round(total_score/(weight_title+weight_tags),4)

			sorted_results = sorted(total.items(), key=operator.itemgetter(1), reverse=True)
			toptotal = [i[0] for i in sorted_results][0:number_results]

			json_array = []
			for result in toptotal:
				score = total[result]
				jsonfile = get_anime(result, allanimelite)
				if result not in set_anime_ids and jsonfile != "not found":
					jsonfile['score'] = score
					json_array.append(jsonfile)
					
			data = json_array
						
	# if Further Filters are chosen
	if hide_ss and query:
		data = hide_sameseries(anime_indexes, data, allanimelite)

	if show or min_rating or time or finished or licensed:
		data = hide_filter(data, allanimelite, show, min_rating, time, finished, licensed)
	
	print(data)
	data = makeListsOfList(data)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, 
		prevsearch=query, prevtags=tag, prevhide_ss=hide_ss, prevtv=tv)

# def fake_most_similiar(positive, negative, matrix, topn) {
# 	for pos in positive:

# 		get_cossim()

	
# }


def get_anime(anime_id, jsonfile):
	# print(anime_id)
	for element in jsonfile:
		# print(element['anime_id'])
		if element['anime_id'] == anime_id:
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
			if entry['anime_id'] not in hide_set:
				new_data.append(entry)

	return new_data

def hide_filter(data, jsonfile, show, min_rating, time, finished, licensed):
	# Filters: TV, Movie, OVA, Special, OVA, Minimum Anime Rating, Time Period
	new_data = []
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

			show_set = set(show)
			show_add = True
			if show:
				if entry['anime_type'] not in show_set:
					# TV, Movie, OVA, Special, OVA 
					show_add = False

			licensed_add = True
			if licensed:
				if entry['anime_licensors'] == "":
					licensed_add = False

			if min_rating_add and time_add and finished_add and show_add and licensed_add:
				new_data.append(entry)

	return new_data

def rocchio(query, relevant, irrelevant,a=.3, b=.3, c=.8, clip = False):
    q0 = query
    if len(relevant)!=0:
        f = lambda i: np.array(relevant)[i]
        dREL = np.fromfunction(np.vectorize(f), (len(relevant),) , dtype=int)
        dREL = np.sum(dREL,axis=0)
    else:
        dREL = 0
      
    if len(irrelevant)!=0:
        f = lambda i: np.array(irrelevant)[i]
        dNREL = np.fromfunction(np.vectorize(f), (len(irrelevant),) , dtype=int)
        dNREL = np.sum(dNREL,axis=0)
    else:
        dNREL = 0    
    
    if len(relevant)!=0 and len(irrelevant)!=0:
        q1 = (a*q0)+(b*(1/len(relevant))*dREL)-(c*((1/len(irrelevant))*dNREL))
    elif len(relevant)==0:
        q1 = (a*q0)-(c*((1/len(irrelevant))*dNREL))
    elif len(irrelevant)==0:
        q1 = (a*q0)+(b*(1/len(relevant))*dREL)

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

