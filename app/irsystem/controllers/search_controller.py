from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import numpy as np
import json
import operator

project_name = "AniAi: Anime Recommender"
net_id = "Arthur Chen (ac2266), Henry Levine (hal59), Kelley Zhang (kz53), Gary Gao (gg392), Cheyenne Biolsi (ckb59)"
# animelite.csv
animelite = json.load(open('data/animelite.json'))


synposis_tfidf = np.load('data/synposis_tfidf.npy')
tags_data = np.load('data/tags.npy')
firstcolumn = synposis_tfidf[:,0]

tags_array = ['action','adventure','cars','comedy','dementia','demons','mystery','drama','ecchi','fantasy','game','hentai','historical','horror','kids','magic','martial_arts','mecha','music','parody','samurai','romance','school','sci-fi','shoujo','shoujo_ai','shounen','shounen_ai','space','sports','super_power','vampire','yaoi','yuri','harem','slice_of_life','supernatural','military','police','psychological','thriller','seinen','josei']
tags_set = set(tags_array)

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	tag = request.args.get('tagsearch')

	if not query and not tag:
		data = []
		output_message = ''

	elif not query and tag: # Need Still Work
		tag_index = -1
		for element in tags_set:
			if element == tag:
				tag_index = tags_array.index(tag)

		if tag_index == -1:
			data = []
			output_message = 'Tag(s) ' + tag + ' do not exist. Pls try again.'
		else:
			output_message = 'You looked for the Tag(s) ' + tag
			mytag = []
			mytag.append(tag_index)
			mytag_set = set(mytag)

			jaccsim_matrix = np.zeros(firstcolumn.size)
			for i in range(firstcolumn.size-1):
				anime_i_tags = np.where(tags_data[i,:] > 0)[0]
				anime_i_set = set(anime_i_tags)
				jaccsim_matrix[i] = get_jaccard(mytag_set, anime_i_set)

			jaccard_order = np.argpartition(jaccsim_matrix, -10)[-10:]
			data = []
			for ind in jaccard_order:
				data.append(animelite[ind])

	elif not tag and query:
		
		anime_index = -1
		for element in animelite:
			if element['anime_english_title'] == query:
				anime_index = element['anime_id']
		
		if anime_index == -1:
			data = []
			output_message = 'Could not find ' + query + '. Please try again pls.'
		else:
			output_message = 'Your search: ' + query + 'meep'
			column_index = np.where(firstcolumn == anime_index)[0][0] 
			cossim = {}
			for i in range(firstcolumn.size):
				cossim[i] = get_sim(column_index, i, synposis_tfidf)

			top10results = dict(sorted(cossim.items(), key=lambda x: x[1], reverse=True)[:11])
			top10results_list = top10results.keys()[1:] #these are column indexes, we need anime ids
			top10animes = firstcolumn[top10results_list]

			json_array = []
			for result in top10animes:
				json_array.append(get_anime(result, animelite))

			data = json_array

	else: # Tag and Anime Still Needs Work

		output_message = "Your search: " + query + 'help' + tag
		anime_index = -1
		for element in animelite:
			if element['anime_english_title'] == query:
				anime_index = element['anime_id']

		tag_index = -1
		for element in tags_set:
			if element == tag:
				tag_index = tags_array.index(tag)

		if anime_index == -1:
			data = []
			output_message = 'Wrong Anime'

		elif tag_index == -1:
			data = []
			output_message = 'Tag(s) ' + tag + ' do not exist. Pls try again.'

		else:
			column_index = np.where(firstcolumn == anime_index)[0][0]
			cossim = {}
			for i in range(firstcolumn.size):
				cossim[i] = get_sim(column_index, i, synposis_tfidf)

			topresults = dict(sorted(cossim.items(), key=lambda x: x[1], reverse=True)[:11])
			topresults_list = topresults.keys()[1:] #these are column indexes, we need anime ids
			# topanimes = firstcolumn[topresults_list] #these are anime ids

			mytag = []
			mytag.append(tag_index)
			mytag_set = set(mytag)

			# jaccsim_matrix = np.zeros(np.array(topresults_list).size)
			jaccsim_matrix = []
			for i in topresults_list:
				anime_i_tags = np.where(tags_data[i,:] > 0)[0]
				anime_i_set = set(anime_i_tags)
				jaccsim_matrix.append(get_jaccard(mytag_set, anime_i_set))

			jaccard_order = np.argpartition(jaccsim_matrix, -10)[-10:]
			data = []
			for ind in jaccard_order:
				data.append(animelite[topresults_list[ind]]) # need column ids

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

def get_anime(anime_id, jsonfile):
	# print(anime_id)
	for element in jsonfile:
		# print(element['anime_id'])
		if element['anime_id'] == anime_id:
			return element
	return "meep"

def get_sim(index, ind2, tfidf):
    """Returns a float giving the cosine similarity of 
       the two movie transcripts.
    
    Params: {mov1: String,
             mov2: String,
             input_doc_mat: Numpy Array,
             movie_name_to_index: Dict}
    Returns: Float (Cosine similarity of the two movie transcripts.)
    """
    # YOUR CODE HERE
    # numpy matrix whose shape is the number of documents by the number of words you're considering max 5000
    queryvector = tfidf[index,:]
    othervector = tfidf[ind2,:]
    numerator = np.dot(queryvector, othervector)
    denominator = (np.dot(np.linalg.norm(queryvector), np.linalg.norm(othervector)))
    return numerator/denominator

def get_jaccard(setA, setB):
	jacsim = len(setA & setB)/len(setA | setB) 
	return jacsim


