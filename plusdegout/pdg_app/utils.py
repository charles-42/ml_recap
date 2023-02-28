def get_spotify_token():
    import requests
    import base64
    from dotenv import load_dotenv
    import os

    load_dotenv()
    ID = os.getenv('ID')
    PSW = os.getenv('PSW')

    # Step 1 - Authorization 
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    # Encode as Base64
    message = f"{ID}:{PSW}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')


    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']

    return token

def get_prediction(token):

    track_id = get_track_id("Le sud",token)
    track_features = get_track_features(track_id,token)
    popularity = call_api(track_features)

    return popularity

def get_track_id(track_name,token): 
    import requests

    params=f'track:{track_name}'

    search_url = f"https://api.spotify.com/v1/search"

    headers = {
        "Authorization": "Bearer " + token
    }

    data = {
        'q' : params,
        'type': 'track',
        'limit': '50',
        'offset': '0',
    }

    res = requests.get(url=search_url, headers=headers, params=data)
    res = res.json()
    id_list = []
    if res.get('tracks'):
        for i  in range(0,len(res['tracks']["items"])) :
            id_list.append(res['tracks']["items"][i]["id"])
        return  id_list[0]
    else:
        return None

def get_track_features(track_id,token):
    import requests
    headers = {
    "Authorization": "Bearer " + token
    }
    featurers_url = f"https://api.spotify.com/v1/audio-features/{track_id}"



    res = requests.get(url=featurers_url, headers=headers)
    return res.json()

def call_api(track_features):
    import requests
    url = "http://0.0.0.0:6000/predict"
    data = dict()
    col = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
       'type', 'duration_ms','time_signature'
       ]

    for feature in col:
        data[feature]= track_features[feature]  

    res = requests.post(url=url, json=data)
    return res.json()

if __name__ == "__main__":
    print(get_spotify_token())
