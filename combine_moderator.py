#!python3
import csv
import sys
from collections import defaultdict

HEADERS = ["key", "input1", "input2", "input3"]
OUTPUT_FILENAME = "moderatorProject_input.csv"

_script_name, input_filename = sys.argv

entries_by_key = defaultdict(list)

with open(input_filename, encoding='utf-8') as csv_file:
    for row in csv.DictReader(csv_file):
        entries_by_key[row["key"]].append(row)

new_input_rows = []
for entries in entries_by_key.values():
    if any(entry["status"] != "done" for entry in entries):
        continue

    #for entry in entries:
    new_input_rows.append(
        [
            entries[0]["key"],
            entries[0]["output1"],
            entries[1]["output1"],
            entries[0]["input1"],
        ]
        )

with open(OUTPUT_FILENAME, mode="w", newline='', encoding="utf-8-sig") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(HEADERS)
    csv_writer.writerows(new_input_rows)

print(f"Done! See the new file '{OUTPUT_FILENAME}'")
