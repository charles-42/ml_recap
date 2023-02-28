import pickle
import pandas as pd
import numpy as np
import sklearn



def predict_pipeline(form_info):
       model = pickle.load(open("app/model.pkl", 'rb'))

       col = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
       'type', 'duration_ms','time_signature'
       ]

       temp = dict(zip(col,form_info))
       to_predict = pd.DataFrame(temp, index=[0])
       popularity = model.predict(to_predict)[0]
       return popularity


       

       #form_info = {'danceability': 0.369, 'energy': 0.126, 'key': 0, 'loudness': -19.68, 'mode': 1, 'speechiness': 0.107, 'acousticness': 0.993, 'instrumentalness': 0.00229, 'liveness': 0.108, 'valence': 0.398, 'tempo': 174.614, 'type': 'audio_features', 'duration_ms': 88920, 'time_signature': 1}

      

       # return loaded_model.predict(df)[0]
        