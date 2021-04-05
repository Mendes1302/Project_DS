# Required libraries
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from pymongo import MongoClient
from datetime import datetime
from tweepy import Stream
import json

# MongoDB access
cluester = MongoClient("your_mongodb+srv")
db = cluester["Twitter"]
collection = db["Covid_in_Brazil"]

# Twitter access token
access_token_secret = "XXXXXXXXXXXXXXXXXXXX"
consumer_secret =     "XXXXXXXXXXXXXXXXXXXX"
consumer_key =        "XXXXXXXXXXXXXXXXXXXX"
access_token =        "XXXXXXXXXXXXXXXXXXXX"


# Twitter access
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Class of get, filter and saved of data 
class MyListener(StreamListener):
    def on_data(self, dados):


        # Variables of control
        control = ["BRASIL", "BRAZIL", "AC","AL",
                    "AP","AM","BA","CE","ES","GO",
                    "MA","MT","MS","MG","PA","PB",
                    "PR","PE","PI","RJ","RN","RS",
                    "RO","RR","SC","SP","SE","TO","DF"]
        b = 0

        # Convert date type (str ---> dict)
        tweet = json.loads(dados)


        # Filter and store data
        if "lang" in tweet and tweet["lang"] == "pt":
            for _ in tweet["user"]:
                if "user" in tweet and "location" in tweet["user"] and tweet["user"]["location"] != None:
                    for i in control:
                        if i in tweet["user"]["location"].upper() and len(tweet["user"]["location"]) > 6 and "id" in tweet and "text" in tweet: 
                            location = tweet["user"]["location"]
                            if len(tweet["text"]) > 0 and len(str(tweet["id"])) > 0:
                                id = tweet["id"]
                                text = tweet["text"]
                                obj = {"id_user":id,"text":text,"location":location,} 
                                b = 1
                                collection.insert_one(obj).inserted_id
                                break
                if b:
                    b = 0
                    break

                else:
                    return True
        return True



while True:
    try:
        # Get data from twitter calling for the class [MyListener]
        mylistener = MyListener()
        mystream = Stream(auth, listener = mylistener)

        # Keywords related to Covid-19
        keywords = ["Sars-Cov-2", "covid", "Sputnik V", "covid-19", "COVID-19", "coronavírus", "CoronaVac", "Pfizer", "Novavax", "CoronaVac", "AstraZeneca"]
        mystream.filter(track=keywords, stall_warnings=True)
    
    except Exception:
        pass

