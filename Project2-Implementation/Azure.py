import os
import csv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticate_client(key,endpoint):
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client


def GetAzureKeyWords(client,source,subreddit,postID):
    try:
        response = client.extract_key_phrases(documents = source)[0]
        if not response.is_error:
            return response.key_phrases
            #for phrase in response.key_phrases:
                #print(phrase)
        else:
            print(">>>>Error while request {}/{}! {}".format(subreddit, postID, response.error))

    except Exception as err:
        print("Azure encountered exception on {}{}. {}".format(subreddit, postID, err))
        

if __name__ == "__main__":
    key = "8385f059169f4a7d9573da65771ac448"
    endpoint = "https://iama-text.cognitiveservices.azure.com/"
    client = authenticate_client(key,endpoint)
    text = "I am a Chef living in Austin, Texas and I recently competed on Season 10 of MasterChef. After losing over 80lbs in one year using the Ketogenic Diet, I was inspired to share my Keto Recipes with the world. The key to my success was that I always enjoyed what I was eating! Losing weight should NEVER be torture. I want to show people how to create stunning meals at home that are also healthy AND delicious! My keto cookbook, “New Keto Cooking” was created for true foodies and will be available on December 8th."
    source = [text]
    subreddit = "r/IAmA"
    postID = "dahz12"
    result = GetAzureKeyWords(client,source,subreddit,postID)
    #keto cookbook
    #Keto Recipes
    #New Keto Cooking
    #home
    #stunning meals
    #true foodies
    #Texas
    #year
    #Ketogenic Diet
    #Season
    #Austin
    #lbs
    #people
    #world
    #key
    #success
    #MasterChef
    #weight