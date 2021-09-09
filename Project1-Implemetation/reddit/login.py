import requests
import datetime

def Ouath2(username, password):
    base_url = 'https://www.reddit.com/'
    data = {'grant_type': 'password', 'username': username, 'password': password}
    auth = requests.auth.HTTPBasicAuth("pbDWeyuQ1CWpNw", "w9tH4f2qi8zbvoHPdwWXqAd596sFZw")
    r = requests.post(base_url + 'api/v1/access_token',
                    data=data,
                    headers={'user-agent': 'DSIAMA by xeoxoe'},
                    auth=auth)
    d = r.json()

    token = 'bearer ' + d['access_token']

    api_url = 'https://oauth.reddit.com'

    headers = {'Authorization': token, 'User-Agent': 'DSIAMA by xeoxoe'}
    response = requests.get(api_url + '/api/v1/me', headers=headers)
    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}    {}".format(response.status_code, response.text, datetime.datetime.now())
    )

    return response.status_code,headers