import csv
import json 
# use python csvhelper.py to create csv file

infile = "AnimeReviews.csv"
outfile = "allanime.csv"

with open(infile, encoding='utf-8') as f, open(outfile, 'w') as o:
	reader = csv.reader(f)
	writer = csv.writer(o, delimiter=',') # adjust as necessary
	animeids = set()
	pls = 0
	for row in reader:
		if row[0] == "anime_id" and pls == 0:
			pls += 1
			writer.writerow(row[0:33])
		else:
			writer.writerow(row[0:33])


with open(outfile, encoding='utf-8') as f, open("allanimelite.csv", 'w') as o:
	reader = csv.reader(f)
	writer = csv.writer(o, delimiter=',') # adjust as necessary
	animeids = set()
	for row in reader:
		row0 = row[0]
		if row0 not in animeids:
			animeids.add(row0)
			writer.writerow(row)

# with open("allanimelite.csv") as f:
#     df = pd.read_csv(f)


# attributes = ["anime_id", "anime_index", "anime_english_title", "anime_japanese_title", "anime_image_url", "anime_genres", "anime_synopsis", "anime_rating_value", "anime_rating_count", "anime_rating", "anime_ranked", "anime_popularity", "anime_favorites", "anime_members", "anime_number_of_episodes", "anime_type", "anime_source", "anime_background", "anime_premiered", "anime_status", "anime_broadcast", "anime_producers", "anime_licensors", "anime_studios", "anime_duration", "anime_side_story", "anime_adaptation", "anime_summary", "anime_full_story", "anime_parent_story", "anime_sequel", "anime_prequel", "anime_alternative_setting", "anime_other"]
# reader = csv.DictReader("allanimelite.csv", )

with open('allanimelite.csv') as f:
	reader = csv.DictReader(f)
	rows = list(reader)

with open('animelite.json', 'w') as f:
	json.dump(rows, f)