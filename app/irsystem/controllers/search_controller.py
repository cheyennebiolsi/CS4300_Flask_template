from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "AniAi: Anime Recommender"
net_id = "Arthur Chen:ac2266, Henry Levine:hal59, Kelley Zhang:kz53, Gary Gao:gg392, Cheyenne Biolsi:ckb59"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



