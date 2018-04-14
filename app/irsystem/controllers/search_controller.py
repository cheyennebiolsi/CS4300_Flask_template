from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import numpy as np
import json

project_name = "AniAi: Anime Recommender"
net_id = "Arthur Chen (ac2266), Henry Levine (hal59), Kelley Zhang (kz53), Gary Gao (gg392), Cheyenne Biolsi (ckb59)"
# animelite.csv
animelite = json.load(open('data/animelite.json'))


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
		data = animelite[0:3]
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

# def rank():




