#!python3
import csv
#import json
import ndjson
import sys
from itertools import groupby

OUTPUT_FILENAME = "import_text_cat.csv"
MAIN_KEY = "sample_data"

#_script_name, input_filename = sys.argv
input_filename = r'Topic_classification_telus_dataset.json'
print(f"Reading from '{input_filename}")

with open(input_filename, encoding='utf-8') as f:
    #content = json.load(f)[MAIN_KEY]
    content = ndjson.load(f)

#sorted_posts = sorted(content, key=lambda entry: (entry["post_id"], entry["post_number"]))
#grouped_posts = groupby(sorted_posts, key=lambda entry: entry["post_id"])


sorted_posts = sorted(content, key=lambda entry: (
    int(entry["topic_id"]), int(entry["text_id"])))
grouped_posts = groupby(sorted_posts, key=lambda entry: entry["topic_id"])


csv_rows = []

for post_id, grouped_post in grouped_posts:
    full_post = ""

    for post in grouped_post:
        #full_post += f"text_id: {post['text_id']}\n{post['raw_text']}\n\n"
        csv_rows.append(
            [f"{post_id}_{post['text_id']}",post['raw_title'], post['raw_text']])

    #csv_rows.append([f"{post_id}_full", full_post])

with open(OUTPUT_FILENAME, mode="w", newline='', encoding="utf-8-sig") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["key", "input1", "input2"])
    csv_writer.writerows(csv_rows)

print(f"Done! Check the new file '{OUTPUT_FILENAME}'")
