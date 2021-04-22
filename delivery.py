import csv
#import json
import ndjson
import sys
from collections import defaultdict

#_script_name, input_json_filename, input_csv_filename = sys.argv
input_csv_filename = r'C:\Scripts\Sentiment_Analysis\Moderator.csv'
input_json_filename = r'C:\Scripts\Sentiment_Analysis\LionBridge.json'
entries_by_key = defaultdict(list)
updated_list = []
full_dict = {}

with open(input_csv_filename, encoding='utf-8') as csv_file:
    for row in csv.DictReader(csv_file):
        entries_by_key[row["key"]].append(row)

for entry in entries_by_key:
    if (entries_by_key[entry][-1]['output1'] != '' and entries_by_key[entry][-1]['status'] == 'done'):
        #Taking -1 as it is the last item within the group
        updated_list.append([entries_by_key[entry][-1]['key'], [entries_by_key[entry][-1]['input1'],entries_by_key[entry][-1]['input2'],entries_by_key[entry][-1]['output1']]])


with open(input_json_filename, 'r', encoding='utf-8') as json_out_file:
    full_json = ndjson.load(json_out_file)#['sample_data']
    for f in range(len(full_json)):
        temp_key = full_json[f]['topic_id']+'_'+full_json[f]['order_within_topic']
        if (full_json[f]['order_within_topic']=='1'):
            for result in updated_list:
                if (temp_key == result[0]):
                    #Get temp key and combine with full, e.g. 201_1 to become 201_full
                    element_to_find = temp_key.split('_')[0]+'_full'
                    #Get array back to list False and True where found the element_to_find
                    overall_sentiment = [element_to_find in sub_list for sub_list in updated_list]
                    if (True in overall_sentiment):
                        full_json[f].update({'sentiment': result[1], 'overall_sentiment': updated_list[overall_sentiment.index(True)][1]})
                    else:
                        full_json[f].update({'sentiment': result[1]})
        else: 
            for result in updated_list:
                if (temp_key == result[0]):
                    full_json[f].update({'sentiment': result[1]})


#full_dict['sample_data'] = full_json


j = ndjson.dumps(full_json).encode('utf8')
with open(input_json_filename, 'wb') as f:      
    f.write(j)


