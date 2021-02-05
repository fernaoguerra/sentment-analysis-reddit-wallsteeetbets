from psaw import PushshiftAPI
import datetime, os
from google.cloud import language_v1

def get_comments(query,subreddit):
    api = PushshiftAPI()
    start_time = int(datetime.datetime(2021, 2, 3).timestamp())
    gen = api.search_comments(after=start_time,q=query, subreddit=subreddit, limit=4)
    average_score = []
    for c in gen:
        print(c.body)
        score = analyze_sentiment(c.body)
        print(score)        
        print("-----------------")
        average_score.append(score)
    print(sum(average_score) / len(average_score))

def analyze_sentiment(text_content):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"
    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = {"content": text_content, "type_": type_, "language": "en"}
    encoding_type = language_v1.EncodingType.UTF8
    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    sentiment = response.document_sentiment.score
    return sentiment

get_comments("#GME","wallstreetbets")