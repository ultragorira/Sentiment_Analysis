import csv
import json
import sys
from collections import defaultdict

#_script_name, input_json_filename, input_csv_filename = sys.argv
input_csv_filename = r'C:\Scripts\Sentiment_Analysis\Moderator.csv'
input_json_filename = r'C:\Scripts\Sentiment_Analysis\sample_data_final.json'
entries_by_key = defaultdict(list)
updated_list = []
full_conv_results = []
full_dict = {}

with open(input_csv_filename, encoding='utf-8') as csv_file:
    for row in csv.DictReader(csv_file):
        entries_by_key[row["key"]].append(row)

for entry in entries_by_key:
    if (entries_by_key[entry][-1]['output1'] != '' and entries_by_key[entry][-1]['key'].find('full')==-1):
        updated_list.append([entries_by_key[entry][-1]['key'], [entries_by_key[entry][-1]['input1'],entries_by_key[entry][-1]['input2'],entries_by_key[entry][-1]['output1']]])
    else:
        full_conv_results.append([entries_by_key[entry][-1]['key'], [entries_by_key[entry][-1]['input1'],entries_by_key[entry][-1]['input2'],entries_by_key[entry][-1]['output1']]])

idx = 0
idx_full = 0

with open(input_json_filename, 'r', encoding='utf-8') as json_out_file:
    full_json = json.load(json_out_file)['sample_data']
    for f in full_json:
        selected_row = (f['post_number'])
        if (f['post_number']=='1'):
            full_json[idx].update({'sentiment': updated_list[idx][1], 'overall_sentiment': full_conv_results[idx_full][1]})
            idx +=1
            idx_full +=1
        else: 
            full_json[idx].update({'sentiment': updated_list[idx][1]})
            idx +=1

full_dict['sample_data'] = full_json


j = json.dumps(full_dict, ensure_ascii=False, indent=4).encode('utf8')
with open(input_json_filename, 'wb') as f:      
    f.write(j)


