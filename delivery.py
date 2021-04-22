import csv
#import json
import ndjson
import sys
from collections import defaultdict
from itertools import groupby

#_script_name, input_json_filename, input_csv_filename = sys.argv
input_csv_filename = r'C:\Scripts\Sentiment_Analysis\Moderator.csv'
input_json_filename = r'C:\Scripts\Sentiment_Analysis\Testjson.json'
entries_by_key = defaultdict(list)
updated_list = []
full_dict = {}

def findTopElement(key_name, full_sorted_and_grouped_list):

    for post_id, grouped_post in groupby(full_sorted_and_grouped_list, key=lambda entry: entry["topic_id"]):
        for post in grouped_post:
            if(key_name.split('_')[0] == post['topic_id']):
                if(key_name.split('_')[1] == post['order_within_topic']):
                    return True
                else:
                    return False


with open(input_csv_filename, encoding='utf-8') as csv_file:
    for row in csv.DictReader(csv_file):
        entries_by_key[row["key"]].append(row)

for entry in entries_by_key:
    if (entries_by_key[entry][-1]['output1'] != '' and entries_by_key[entry][-1]['status'] == 'done'):
        #Taking -1 as it is the last item within the group
        updated_list.append([entries_by_key[entry][-1]['key'], [entries_by_key[entry][-1]['input1'],entries_by_key[entry][-1]['input2'],entries_by_key[entry][-1]['output1']]])


with open(input_json_filename, 'r', encoding='utf-8') as json_out_file:
    full_json = ndjson.load(json_out_file)#['sample_data']
    sorted_posts = sorted(full_json, key=lambda entry: (int(entry["topic_id"]), int(entry["order_within_topic"])))
    #grouped_posts = groupby(sorted_posts, key=lambda entry: entry["topic_id"])
    for f in range(len(full_json)):
        temp_key = full_json[f]['topic_id']+'_'+full_json[f]['order_within_topic']
        isFirst = findTopElement(temp_key, sorted_posts)
        if (isFirst):
            for result in updated_list:
                if (temp_key == result[0]):
                    #Get temp key and combine with full, e.g. 201_1 to become 201_full
                    element_to_find = temp_key.split('_')[0]+'_full'
                    #Get array back to list False and True where found the element_to_find
                    overall_sentiment = [element_to_find in sub_list for sub_list in updated_list]
                    if (True in overall_sentiment):
                        full_json[f].update({'sentiment': result[1], 'overall_sentiment': updated_list[overall_sentiment.index(True)][1]})
                        break
                    else:
                        full_json[f].update({'sentiment': result[1]})
                        break
        else: 
            for result in updated_list:
                if (temp_key == result[0]):
                    full_json[f].update({'sentiment': result[1]})
                    break


#full_dict['sample_data'] = full_json


j = ndjson.dumps(full_json).encode('utf-8')
with open(input_json_filename, 'wb') as f:      
    f.write(j)


