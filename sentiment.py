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

tokenizer = TweetTokenizer()

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
    'zero'
]

english_plus2 = english_plus + ["episodes", "art", "character", "anime", "series", "watched", "watch", "num", "num0", "NUM", "NUM0"]

# Create Count Vectorizer 
for 
	cvect = CountVectorizer(stop_words=english_plus2, min_df=20, max_df = 0.95, max_features =200, ngram_range=(1,2))
	X = cvect.fit_transform(df[df.anime_english_title == "Naruto"]["review_text"])
	terms = cvect.get_feature_names()
	pmi_matrix = getcollocations_matrix(X)
	reviews_pos_tagged=[pos_tag(tokenizer.tokenize(m)) for m in df[df.anime_english_title == "Naruto"]["review_text"]]
	reviews_adj_adv_only=[" ".join([w for w,tag in m if tag in ["JJ","RB","RBS","RBJ","JJR","JJS"]])
	                      for m in reviews_pos_tagged]
	X = cvect.fit_transform(reviews_adj_adv_only)
	terms = cvect.get_feature_names()
	pmi_matrix=getcollocations_matrix(X)

	posscores=seed_score(['good','great','perfect','cool', "amazing", "enjoyable", "favorite", "worth", "greatest", "awesome", "beautiful", "deep", "unique", "nice", "funny"])
	negscores=seed_score(['bad','terrible','wrong',"crap","long","boring", "stupid", "worst", "slow", "useless", "old", "terrible", "filler"])

	sentscores={}
	for w in terms:
	    sentscores[w] = posscores[w] - negscores[w]

	meep = sorted(sentscores.items(),key=operator.itemgetter(1),reverse=False)
	bottom5 = meep[:5]
	top5 = meep[-5:]
	



def getcollocations_matrix(X):
    XX=X.T.dot(X)  ## multiply X with it's transpose to get number docs in which both w1 (row) and w2 (column) occur
    term_freqs = np.asarray(X.sum(axis=0)) ## number of docs in which a word occurs
    pmi = XX.toarray() * 1.0  ## Casting to float, making it an array to use simple operations
    pmi /= term_freqs.T ## dividing by the number of documents in which w1 occurs
    pmi /= term_freqs  ## dividing by the number of documents in which w2 occurs
    
    return pmi  # this is not technically PMI beacuse we are ignoring some normalization factor and not taking the log 
                # but it's sufficient for ranking

def getcollocations(w,PMI_MATRIX=pmi_matrix,TERMS=terms):
    if w not in TERMS:
        return []
    idx = TERMS.index(w)
    col = PMI_MATRIX[:,idx].ravel().tolist()
    return sorted([(TERMS[i],val) for i,val in enumerate(col)],key=operator.itemgetter(1),reverse=True)

def seed_score(pos_seed,PMI_MATRIX=pmi_matrix,TERMS=terms):
    score=defaultdict(int)
    for seed in pos_seed:
        c=dict(getcollocations(seed,PMI_MATRIX,TERMS))
        for w in c:
            score[w]+=c[w]
    return score