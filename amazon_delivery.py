#!python3
import csv
import sys
from itertools import groupby

import ndjson


OUTPUT_FILENAME = "LionBridge_SentimentAnalysis_Final_Delivery.json"

topic_first_posts = {}


def read_customer_file(filepath):
    print(f"Reading from customer file '{customer_file}'")
    with open(customer_file, encoding="utf-8") as f:
        customer_content = ndjson.load(f)

    sorted_customer_content = sorted(
        customer_content, key=lambda entry: (entry["topic_id"], entry["order_within_topic"])
    )
    grouped_customer_content = groupby(
        sorted_customer_content, key=lambda entry: entry["topic_id"]
    )

    for key, entries in grouped_customer_content:
        topic_first_posts[key] = f"{key}_{list(entries)[0]['order_within_topic']}"

    return customer_content


def read_annotation_file(filepath):
    """
    Returns a dict of {item_key: last_pass_item]}
    """
    print(f"Reading from annotation file '{annotation_file}'")

    with open(annotation_file, encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        sorted_items = sorted((item for item in csv_reader), key=lambda item: item["ctime"])

    grouped_items = groupby(sorted_items, lambda item: item["key"])

    last_pass_items_by_key = {}
    for key, items in grouped_items:
        last_pass_items_by_key[key] = list(items)[-1]

    return last_pass_items_by_key


def item_results(item):
    return [item["input1"], item["input2"], item["output1"]]


def save_result(delivery_items):
    with open(OUTPUT_FILENAME, mode="w", newline="", encoding="utf-8") as output_file:
        ndjson.dump(delivery_items, output_file)


_script_name, customer_file, annotation_file = sys.argv

annotation_dict = read_annotation_file(annotation_file)
delivery_items = []

for customer_entry in read_customer_file(customer_file):
    item_key = f'{customer_entry["topic_id"]}_{customer_entry["order_within_topic"]}'

    try:
        item = annotation_dict[item_key]
    except KeyError:
        print(f"Item key '{item_key}' not found in the items")
        continue

    customer_entry["sentiment"] = item_results(item)
    delivery_items.append(customer_entry)

    """ if topic_first_posts[customer_entry["topic_id"]] == item_key:
        item_full = annotation_dict[f'{customer_entry["topic_id"]}_full']
        customer_entry["overall_sentiment"] = item_results(item_full) """


save_result(delivery_items)

print(f"Done! Check the new file '{OUTPUT_FILENAME}'")
