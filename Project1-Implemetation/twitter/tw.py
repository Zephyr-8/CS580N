from pymongo import MongoClient
import datetime
import time
import requests
import os
import json

def get_auth():
    #return os.environ.get("BEARER_TOKEN")
    return "AAAAAAAAAAAAAAAAAAAAAMCaJQEAAAAAOtve0U8d3RG%2"+"FfsWZUx4CswWGT18%3DwQxfDdVXA2dQNXHP5ANYAeiYmPbqt5lirFjLt3jCG4NCSDMAxo"

def create_url():
    #return "https://stream.twitter.com/1.1/statuses/sample"
    return "https://api.twitter.com/2/tweets/sample/stream"

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def set_request_parameters():
    params = {'tweet.fields':'created_at,public_metrics,entities','expansions':'author_id,attachments.media_keys','user.fields':'id,name,username','media.fields':'preview_image_url'}
    return params

def get_sample_stream(url, headers,params,db):
    response = requests.request("GET", url, headers=headers, stream=True, params=params)
    print(response.status_code)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            #print(json.dumps(json_response, indent=4, sort_keys=True))
            dt=datetime.datetime.fromisoformat(json_response['data']['created_at'][:-1])
            time_stamp=round(dt.timestamp())
            #print(time_stamp)
            data={
                'tweet_id':json_response['data']['id'],
                'time_stamp':time_stamp,
                'author_id':json_response['data']['author_id'],
                'text':json_response['data']['text'],
                'like_count':json_response['data']['public_metrics']['like_count'],
                #'quote_count':json_response['data']['public_metrics']['quote_count'],
                #'reply_count':json_response['data']['public_metrics']['reply_count'],
                'retweet_count':json_response['data']['public_metrics']['retweet_count'],
            }

            #collect hashtags
            if 'entities' in json_response['data'] and 'hashtags' in json_response['data']['entities']:
                hashtags=[]
                for item in json_response['data']['entities']['hashtags']:
                    if item['tag'] not in hashtags:
                        hashtags.append(item['tag'])
                #print(hashtags)
                for tag in hashtags:
                    hashtag_data={
                                'hashtag_name':tag,
                                'tweet_id':json_response['data']['id']
                                }
                    #print(json.dumps(hashtag_data,indent=4, sort_keys=False))
                    try:
                        db.hashtag_collection.insert_one(hashtag_data)
                    except:
                        print("Exception of inserting data to hashtag_collection!")

                data['hashtags']=hashtags
            else:
                data['hashtags']=None
            
            #collect media
            if 'media' in json_response['includes']:
                media_urls=[]
                media_keys=[]
                for item in json_response['includes']['media']:
                        if 'preview_image_url' in item:                  
                            media_urls.append(item['preview_image_url'])
                        if 'media_key' in item:
                            media_keys.append(item['media_key'])
                data['media_keys']=media_keys
                if len(media_urls)!=0:
                    data['image_urls']=media_urls
                else:
                    data['image_urls']=None
            else:
                data['media_keys']=None
                data['image_urls']=None

            try:
                #print(json.dumps(data,indent=4, sort_keys=False))
                db.twitter_collection.insert_one(data)
            except:
                print("Exception of inserting data to twitter_collection!")
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

def main():
    client = MongoClient('localhost', 27017)
    db = client.twitter_db
    bearer_token=get_auth()
    params=set_request_parameters()
    url=create_url()
    headers=create_headers(bearer_token)
    get_sample_stream(url,headers,params,db)

if __name__=="__main__":
	main()
