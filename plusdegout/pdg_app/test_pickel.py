import pickle
import pandas as pd
import sklearn

loaded_model = pickle.load(open("pdg_app/model.pkl", 'rb'))

features_list = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
       'type', 'duration_ms','time_signature'
       ]

df = pd.DataFrame(columns = features_list)

form_info = {'danceability': 0.369, 'energy': 0.126, 'key': 0, 'loudness': -19.68, 'mode': 1, 'speechiness': 0.107, 'acousticness': 0.993, 'instrumentalness': 0.00229, 'liveness': 0.108, 'valence': 0.398, 'tempo': 174.614, 'type': 'audio_features', 'duration_ms': 88920, 'time_signature': 1}

df.loc[0] = form_info

result = loaded_model.predict(df)
print(result)