import sys
import csv
import tweepy
import matplotlib.pyplot as plt

from collections import Counter
from aylienapiclient import textapi  # (to analyze the sentiment of the Tweets)

if sys.version_info[0] < 3:
    input = raw_input

## Twitter credentials
# # Consume:
# CONSUMER_KEY    = 'CrMSxqJz6zvwEa85OOKdUpSeH'
# CONSUMER_SECRET = 'hkdYe8u9SB30Y67uY9RdqRwrh00gZyFedYHI4iyFziRDeVjPxx'

# # Access:
# ACCESS_TOKEN  = '3093984751-BpI2Oat6hRf8qEWuIfKlz3Hrn8vsPm3KjOn6GvF'
# ACCESS_SECRET = 'tISJPGvRQ2TZJhKuNA0HZ9kORuS699gsnsVzoh7YV8rUU'
consumer_key = "CrMSxqJz6zvwEa85OOKdUpSeH"
consumer_secret = "hkdYe8u9SB30Y67uY9RdqRwrh00gZyFedYHI4iyFziRDeVjPxx"
access_token = "3093984751-BpI2Oat6hRf8qEWuIfKlz3Hrn8vsPm3KjOn6GvF"
access_token_secret = "tISJPGvRQ2TZJhKuNA0HZ9kORuS699gsnsVzoh7YV8rUU"

## AYLIEN credentials
application_id = "fa72e110"
application_key = "f309de691e147494feaa3426c63ce649"

## set up an instance of Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

## set up an instance of the AYLIEN Text API
client = textapi.Client(application_id, application_key)

## search Twitter for something that interests you
query = input("What subject do you want to analyze for this example? \n")
number = input("How many Tweets do you want to analyze? \n")

results = api.search(
    lang="en",
    q=query + " -rt",
    count=number,
    result_type="recent"
)

print("--- Gathered Tweets \n")

## open a csv file to store the Tweets and their sentiment
file_name = 'Sentiment_Analysis_of_{}_Tweets_About_{}.csv'.format(number, query)

with open(file_name, 'w', newline='') as csvfile:
    csv_writer = csv.DictWriter(

        f=csvfile,
        fieldnames=["Tweet", "Sentiment"]
    )
    csv_writer.writeheader()

    print("--- Opened a CSV file to store the results of your sentiment analysis... \n")

    ## tidy up the Tweets and send each to the AYLIEN Text API
    for c, result in enumerate(results, start=1):
        tweet = result.text
        tidy_tweet = tweet.strip().encode('ascii', 'ignore')
        print("Analyzed Tweet {} \n".format(c))
        print(result.user,"\n",result.text,"\n\n")
        if len(tweet) == 0:
            print('Empty Tweet')
            continue

        response = client.Sentiment({'text': tidy_tweet})
        csv_writer.writerow({
            'Tweet': response['text'],
            'Sentiment': response['polarity']
        })


## count the data in the Sentiment column of the CSV file
with open(file_name, 'r') as data:
    counter = Counter()
    for row in csv.DictReader(data):
        counter[row['Sentiment']] += 1

    positive = counter['positive']
    negative = counter['negative']
    neutral = counter['neutral']

## declare the variables for the pie chart, using the Counter variables for "sizes"
colors = ['green', 'red', 'grey']
sizes = [positive, negative, neutral]
labels = 'Positive', 'Negative', 'Neutral'

## use matplotlib to plot the chart
plt.pie(
    x=sizes,
    autopct='%1.1f%%',
    colors=colors,
    labels=labels,
    startangle=90,
    explode = (0.2, 0, 0),
    shadow=True,

)

plt.title("Sentiment of {} Tweets about {}".format(number, query))
file_Savename = 'Sentiment_Analysis_of_{}_Tweets_About_{}.png'.format(number, query)
plt.savefig(file_Savename)
plt.show()
