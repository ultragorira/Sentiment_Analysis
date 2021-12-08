import csv
from csv import DictReader
import boto3
import sys

_script_name, input_file = sys.argv


HEADERS = ["key", "Sentiment", "Positive", "Negative", "Neutral", "Mixed"]
OUTPUT_FILENAME = "ComprehendResults.csv"

#Using boto3 to call the Comprehend API
client = boto3.client('comprehend')

def checkSentiment(text):

    #Sentiment Analysis
    print('Analyzing... ' + text[0])
    try: 
        sentiment = client.detect_sentiment(Text = text[1], LanguageCode = 'en') #API call for sentiment analysis
        sentRes = sentiment['Sentiment'] #Positive, Neutral, or Negative
        sentScore = sentiment['SentimentScore'] #Percentage of Positive, Neutral, and Negative
        #print(sentRes)
        #print(sentScore)
        return([text[0], sentRes[0:3], sentScore['Positive'], sentScore['Negative'], sentScore['Neutral'], sentScore['Mixed']])
    except Exception:
        print(f'Comprehend could not process {text[0]}')
        return([text[0], 'Too long text', 'Too long text', 'Too long text', 'Too long text', 'Too long text'])
def checkEntities(text):

    #Entity Extraction
    entities = client.detect_entities(Text = text, LanguageCode = 'en') #API call for entity extraction
    entities = entities['Entities'] #all entities
    print(entities)
    textEntities = [dict_item['Text'] for dict_item in entities] #the text that has been identified as entities
    typeEntities = [dict_item['Type'] for dict_item in entities] #the type of entity the text is
    print(textEntities)
    print(typeEntities)

comprehend_results = []

with open(input_file, 'r', encoding="utf-8") as f:
    csv_reader = DictReader(f)
    for row in csv_reader:
        comprehend_results.append(checkSentiment([row['key'], row['input1']]))

#print(comprehend_results)
with open(OUTPUT_FILENAME, mode="w", newline='', encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(HEADERS)
    csv_writer.writerows(comprehend_results)

print(f"Done! See the new file '{OUTPUT_FILENAME}'")
