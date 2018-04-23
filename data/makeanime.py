import csv
import ast

# use python csvhelper.py to create csv file

infile = "AnimeReviews3.csv"
outfile = "anime.csv"

with open(infile, encoding='utf-8') as f, open(outfile, 'w') as o:
	reader = csv.reader(f)
	writer = csv.writer(o, delimiter=',') # adjust as necessary
	animeids = set()
	for row in reader:
		if row[0] != "anime_id":
			writer.writerow(row[0:33])
		else:
			writer.writerow(row[0:33])