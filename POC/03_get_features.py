def get_features(df,name):
    import requests
    import pandas as pd
    from utils import get_spotify_token
    token = get_spotify_token()

    df_final = pd.DataFrame(columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature'])

    headers = {
    "Authorization": "Bearer " + token
    }
    featurers_url = f"https://api.spotify.com/v1/audio-features/"
    count = 0
    for i in range(0,len(df.id),100):  # len(df.id)
        ids_list=""
        for id in df.id.iloc[i:i+99]:
            ids_list += ","+str(id)

        data = {'ids' : ids_list[1:]}
        res = requests.get(url=featurers_url, headers=headers, params=data)
        for j in range(len(res.json()['audio_features'])):
            if res.json()['audio_features'][j]:
                features_list = res.json()['audio_features'][j].values()
                df_final.loc[len(df_final)] = features_list
        print(i)
        count+=1
        if count%100==0:
            df_final.to_csv(f"features_{name}.csv") 
    df_final.to_csv(f"features_{name}.csv")




if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("tracks_2022_01_01_2022_01_31.csv")
    df_truc = df.loc[69741:]
    get_features(df_truc,"2022_01_01_2022_01_31_part_2")