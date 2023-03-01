import requests



url = "http://0.0.0.0/predict"



data = {'danceability': 0.369, 'energy': 0.126, 'key': 0, 'loudness': -19.68, 'mode': 1, 'speechiness': 0.107, 'acousticness': 0.993, 'instrumentalness': 0.00229, 'liveness': 0.108, 'valence': 0.398, 'tempo': 174.614, 'type': 'audio_features', 'duration_ms': 88920, 'time_signature': 1}


res = requests.post(url=url, json=data)
# res = res.json()

print(res.text)