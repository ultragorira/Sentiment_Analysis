#!python3
import csv
import json
import sys
from itertools import groupby

OUTPUT_FILENAME = "import.csv"
MAIN_KEY = "sample_data"

_script_name, input_filename = sys.argv

print(f"Reading from '{input_filename}")

with open(input_filename, encoding='utf-8') as f:
    content = json.load(f)[MAIN_KEY]

sorted_posts = sorted(content, key=lambda entry: (entry["post_id"], entry["post_number"]))
grouped_posts = groupby(sorted_posts, key=lambda entry: entry["post_id"])

csv_rows = []

for post_id, grouped_post in grouped_posts:
    full_post = ""

    for post in grouped_post:
        full_post += f"response_id: {post['response_id']}\n{post['text']}\n\n"
        csv_rows.append([f"{post_id}_{post['post_number']}", post["text"]])

    csv_rows.append([f"{post_id}_full", full_post])

with open(OUTPUT_FILENAME, mode="w", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["key", "input1"])
    csv_writer.writerows(csv_rows)

print(f"Done! Check the new file '{OUTPUT_FILENAME}'")
