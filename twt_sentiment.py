import tweepy
from textblob import TextBlob
import wordcloud
import pandas as pd
import re
import matplotlib.pyplot as plt

#function to clean the text
def clean(text):
    text=re.sub(r'@[A-Za-z0-9]+','',text)   #removes mentions
    text=re.sub(r'#','',text)               #removes hashtag
    text=re.sub(r'RT[\s]','',text)          #removes retweets
    text=re.sub(r'https?:\/\/\S+','',text)  #removes links
    return text

#function to get the subjectivity of a tweet
def getSubj(text):
    return TextBlob(text).sentiment.subjectivity

#function to get the polarity of a tweet
def getPol(text):
    return TextBlob(text).sentiment.polarity

#function to classify a tweet as positive, negative or neutral
def getAnalysis(score):
    if score<0:
        return 'Negative'
    elif score==0:
        return 'Neutral'
    else:
        return 'Positive'

#twitter API developer credentials
consumerKey='OyTAKIpHQDCfjqmgEYaM7rpEE'
consumerSecret='XXXX'
accessToken='1678414008502632449-E8k7lnfrtLg0U4NelYhfLyapD3bK0U'
accessTokenSecret='XXXX'

#create authentication
authenticate=tweepy.OAuthHandler(consumerKey, consumerSecret)
authenticate.set_access_token(accessToken, accessTokenSecret)
api=tweepy.API(authenticate,wait_on_rate_limit=True)

#extract 10 tweets from user handle "taylorswift13"
posts=api.user_timeline(user_id="taylorswift13",count=10,tweet_mode="extended")

#Insert the extracted tweets into a dataframe
df=pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

#Cleaning the data
df['Tweets']=df['Tweets'].apply(clean)

#Finding the polarity and subjectivity
df['Subjectivity']=df['Tweets'].apply(getSubj)
df['Polarity']=df['Tweets'].apply(getPol)

#creating a word cloud using all extracted words
allWords=''.join([twts for twts in df['Tweets']])
wordCloud=wordcloud(width=500, height=300, random_state=21, max_font_size=119).generate(allWords)
plt.imshow(wordCloud, interpolation="bilinear")
plt.axis('off')
plt.show()

df['Analysis']=df['Polarity'].apply(getAnalysis)

#plotting a graph based on polarity
plt.figure(figsize=(8,6))
for i in range(0,df.shape[0]):
    plt.scatter(df['Polarity'][i],df['Subjectivity'][i],color='Blue')
plt.title('Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()
