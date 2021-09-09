import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions


def GetAuthenticator(key):
    return IAMAuthenticator(key)

def GetWatsonCategries(source, subreddit, postID, authenticator):
    """
    Get categries from IBM Watson.
    Only return categries score over 0.5, if no response fits, return error whits postID
    """
    flag = False

    response=[]
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2020-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url('https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/05e41610-4ce4-473e-84f9-b94679fe9841')

    try:
        response = natural_language_understanding.analyze(
            text=source,
            features=Features(categories=CategoriesOptions(limit=3)))
        if response.get_status_code() == 200:
            response=response.get_result()
        else:
            print(">>>>Error while request {}/{}! {}".format(subreddit, postID, response.get_headers()))
    except Exception as err:
        print("Watson encountered exception on {}/{}. {}".format(subreddit, postID, err))
        result = "IBM Watson bad result"
        return result

    category = response['categories']
    result=""
    for i in category:
        if flag:
            break
        if i['score'] >= 0.5:
            result = i['label']
            flag = True
    if not flag:
        result = "IBM Watson bad result"
        print(">>>>No good category return for %s/%s! Consider using Reddit flag." %(subreddit,postID))

    return result


if __name__ == "__main__":
    text = "Winter is coming, Reddit! Let's talk about how to protect your skin. I'm Board Certified Dermatologist Dr. Valerie Harvey, and I want to answer all your questions about cold weather skincare. Ask Me Anything!"
    subreddit = "r/IAmA"
    postID = "dada12"
    key="DS-mbwwNwqAXVGJONGbzokI5Z6Y_YhDlfzKUKIgYGu-A"
    authenticator = GetAuthenticator(key)
    GetWatsonCategries(text,subreddit,postID,authenticator)
    #/style and fashion/beauty

    text = "Winter is coming"
    subreddit = "r/IAmA"
    postID = "dada12"
    GetWatsonCategries(text,subreddit,postID,authenticator)
    #>>>>No good category return for r/IAmA/dada12! Consider using Reddit flag.