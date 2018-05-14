import pandas as pd
import numpy as np
import operator
import re
import codecs
import tokenize
from nltk.tokenize import TweetTokenizer
from nltk import FreqDist,pos_tag
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from collections import defaultdict
from bs4 import BeautifulSoup
import json
import csv

tokenizer = TweetTokenizer()


poop = np.genfromtxt('idToIndex.csv', delimiter=",")
poop2 = np.delete(poop, 0, 0)
anime_id_column = poop2[:,0]

with codecs.open("AnimeReviews.csv") as f:
	df = pd.read_csv(f)

# def preprocessed(s):
#     return lambda s: re.sub(r'(\d[\d\.])+', 'NUM', s.lower())

english_plus = [
	'a',
	'about',
	'above',
	'after',
	'again',
	'against',
	'all',
	'am',
	'an',
	'and',
	'any',
	'are',
	"aren't",
	'as',
	'at',
	'be',
	'because',
	'been',
	'before',
	'being',
	'below',
	'between',
	'both',
	'but',
	'by',
	"can't",
	'cannot',
	'could',
	"couldn't",
	'did',
	"didn't",
	'do',
	'does',
	"doesn't",
	'doing',
	"don't",
	'down',
	'during',
	'each',
	'few',
	'for',
	'from',
	'further',
	'had',
	"hadn't",
	'has',
	"hasn't",
	'have',
	"haven't",
	'having',
	'he',
	"he'd",
	"he'll",
	"he's",
	'her',
	'here',
	"here's",
	'hers',
	'herself',
	'him',
	'himself',
	'his',
	'how',
	"how's",
	'i',
	"i'd",
	"i'll",
	"i'm",
	"i've",
	'if',
	'in',
	'into',
	'is',
	"isn't",
	'it',
	"it's",
	'its',
	'itself',
	"let's",
	'me',
	'more',
	'most',
	"mustn't",
	'my',
	'myself',
	'no',
	'nor',
	'not',
	'of',
	'off',
	'on',
	'once',
	'only',
	'or',
	'other',
	'ought',
	'our',
	'ours',
	'ourselves',
	'out',
	'over',
	'own',
	'same',
	"shan't",
	'she',
	"she'd",
	"she'll",
	"she's",
	'should',
	"shouldn't",
	'so',
	'some',
	'such',
	'than',
	'that',
	"that's",
	'the',
	'their',
	'theirs',
	'them',
	'themselves',
	'then',
	'there',
	"there's",
	'these',
	'they',
	"they'd",
	"they'll",
	"they're",
	"they've",
	'this',
	'those',
	'through',
	'to',
	'too',
	'under',
	'until',
	'up',
	'very',
	'was',
	"wasn't",
	'we',
	"we'd",
	"we'll",
	"we're",
	"we've",
	'were',
	"weren't",
	'what',
	"what's",
	'when',
	"when's",
	'where',
	"where's",
	'which',
	'while',
	'who',
	"who's",
	'whom',
	'why',
	"why's",
	'with',
	"won't",
	'would',
	"wouldn't",
	'you',
	"you'd",
	"you'll",
	"you're",
	"you've",
	'your',
	'yours',
	'yourself',
	'yourselves',
	'zero',
	'previously',
	'1',
	'2',
	'3',
	'4',
	'5',
	'6',
	'7',
	'8',
	'9',
	'10',
	'ive',
	'didn',
	'back',
	'time'
]



english_plus2 = english_plus + ["episodes", "art", "character", "anime", "series", "watched", "watch", "num", "num0", "NUM", "NUM0"]
def getcollocations_matrix(X):
	XX=X.T.dot(X)  ## multiply X with it's transpose to get number docs in which both w1 (row) and w2 (column) occur
	term_freqs = np.asarray(X.sum(axis=0)) ## number of docs in which a word occurs
	pmi = XX.toarray() * 1.0  ## Casting to float, making it an array to use simple operations
	pmi /= term_freqs.T ## dividing by the number of documents in which w1 occurs
	pmi /= term_freqs  ## dividing by the number of documents in which w2 occurs
	
	return pmi  # this is not technically PMI beacuse we are ignoring some normalization factor and not taking the log 
				# but it's sufficient for ranking

def getcollocations(w,PMI_MATRIX,TERMS):
	if w not in TERMS:
		return []
	idx = TERMS.index(w)
	col = PMI_MATRIX[:,idx].ravel().tolist()
	return sorted([(TERMS[i],val) for i,val in enumerate(col)],key=operator.itemgetter(1),reverse=True)

def seed_score(pos_seed,PMI_MATRIX,TERMS):
	score=defaultdict(int)
	for seed in pos_seed:
		c=dict(getcollocations(seed,PMI_MATRIX,TERMS))
		for w in c:
			score[w]+=c[w]
	return score

# Create Count Vectorizer 
csv_array = []
# with open('poop.json', 'w') as outfile:


# with open(infile, encoding='utf-8') as f, open(outfile, 'w') as o:
# 	reader = csv.reader(f)
# 	writer = csv.writer(o, delimiter=',') # adjust as necessary

# 	for row in reader:
# 		# print('hi'+row[7])
# 		if row[0] != "age":

# 			for i in range(0,16):
# 				row_i = row[i]
# 				# row_i = row_i.replace('<br />',' ')
# 				row_i = row_i.replace('\n','')
# 				row_i = row_i.replace('\t','')
# 				row_i = cleanhtml(row[i])
# 				row[i] = row_i

# 			writer.writerow(row)
# 		else:
# 			writer.writerow(row)
with open('poop.csv', "w") as csv_file:
        # for line in data:
        #     writer.writerow(line)
	writer = csv.writer(csv_file, delimiter=',')
	# json_array = []
	for counter, anime_idx in enumerate(anime_id_column):
		try:
			cvect = CountVectorizer(stop_words=english_plus2, max_df = .75, max_features =200, ngram_range=(1,1))
			reviews_pos_tagged=[pos_tag(tokenizer.tokenize(m)) for m in df[df.anime_id == anime_idx]["review_text"]]
			reviews_adj_adv_only=[" ".join([w for w,tag in m if tag in ["JJ","JJR","JJS"]])
								  for m in reviews_pos_tagged]
			
			X = cvect.fit_transform(reviews_adj_adv_only)
		except:
			# dict_json = {'anime_id':anime_idx, 'anime_index': counter, 'positive':"", 'negative':""}
			writer.writerow(["Review Text Too Short For Sentiment Analysis"])
			continue
		terms = cvect.get_feature_names()
		pmi_matrix=getcollocations_matrix(X)
		
		posscores=seed_score(['good','great','perfect','cool', "amazing", "enjoyable", "favorite", "worth", "greatest", "awesome", "beautiful", "deep", "unique", "nice", "funny"],pmi_matrix,terms)
		negscores=seed_score(['worthless','stiff','shyly','bad','unnecessary','terrible','wrong',"crap","long","boring", "stupid", "worst", "slow", "useless", "old", "terrible", "filler", "miserably"],pmi_matrix,terms)

		sentscores={}
		for w in terms:
			sentscores[w] = posscores[w] - negscores[w]

		meep = sorted(sentscores.items(),key=operator.itemgetter(1),reverse=False)
		# bottom5 = meep[:5]
		top5 = meep[-3:]
		totalwords2 = ""
		for word2 in top5:
			totalwords2 = totalwords2 + word2[0] + "|"
		totalwords2[:-1]
		# dict_json = {'anime_id':anime_idx, 'anime_index': counter, 'positive':totalwords2}
		writer.writerow([totalwords2])
		# json_array.append(dict_json)

	# json.dump(json_array, outfile, indent=4)



