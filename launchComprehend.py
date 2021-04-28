from csv import DictReader
import boto3

#Using boto3 to call the Comprehend API
client = boto3.client('comprehend')

def checkSentiment(text):

    #Sentiment Analysis
    sentiment = client.detect_sentiment(Text = text, LanguageCode = 'en') #API call for sentiment analysis
    sentRes = sentiment['Sentiment'] #Positive, Neutral, or Negative
    sentScore = sentiment['SentimentScore'] #Percentage of Positive, Neutral, and Negative
    print(sentRes)
    print(sentScore)
    
def checkEntities(text):

    #Entity Extraction
    entities = client.detect_entities(Text = text, LanguageCode = 'en') #API call for entity extraction
    entities = entities['Entities'] #all entities
    print(entities)
    textEntities = [dict_item['Text'] for dict_item in entities] #the text that has been identified as entities
    typeEntities = [dict_item['Type'] for dict_item in entities] #the type of entity the text is
    print(textEntities)
    print(typeEntities)

input_file = 'ComprehendInput.csv'

with open(input_file, 'r', encoding="utf-8") as f:
    csv_reader = DictReader(f)
    for row in csv_reader:
        checkSentiment(row['input3'])

#checkSentiment()
#checkEntities()