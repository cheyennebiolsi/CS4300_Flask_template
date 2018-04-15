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
firstcolumn = synposis_tfidf[:,0]

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	tag = request.args.get('tagsearch')
	if not query and not tag:
		data = []
		output_message = ''
	# elif not query and tag:
	# 	data = range(5)
	# 	output_message = 'tag'
	# elif not tag and query:
	# 	data = range(6,9)
	# 	output_message = 'tag' 
	else:
		output_message = "Your search: " + query
		anime_index = 0
		for element in animelite:
			if element['anime_english_title'] == query:
				anime_index = element['anime_id']
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

		# data = animelite[0:6]
		data = json_array
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



