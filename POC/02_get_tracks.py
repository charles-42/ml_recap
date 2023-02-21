def get_album_tracks(album_name,token): 
    import requests

    params=f'album:{album_name} AND year:2022'

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
    popularity_list = []
    id_list = []
    name_list = []
    if res.get('tracks'):
        for i  in range(0,len(res['tracks']["items"])) :
            popularity_list.append(res['tracks']["items"][i]["popularity"])
            id_list.append(res['tracks']["items"][i]["id"])
            name_list.append(res['tracks']["items"][i]["name"])
        return popularity_list, id_list, name_list
    else:
        return None,None,None

def get_tracks(df,limit=None, start=0,name):

    if not limit:
        limit = len(df)
    import pandas as pd
    import time
    df_final = pd.DataFrame(columns=["id","popularity",'names'])

    from utils import get_spotify_token
    token = get_spotify_token()
    count = 0
    for album in df["title"].iloc[start:limit]:
        count+=1
        time.sleep(0.1)
        
    
        popularity_list, id_list, name_list = get_album_tracks(album,token)
        
        if popularity_list:
            df = pd.DataFrame({'id' : id_list, 'popularity' : popularity_list, 'names': name_list}, index=range(len(id_list)))
            df_final = pd.concat([df_final,df])

        if count%10 == 0:
            print(count)

        if count%100 ==0:
            df_final.to_csv("tracks_partial.csv")
            
            print(df_final.tail(1))

    df_final.to_csv(f"tracks_{name}.csv")


if __name__ == "__main__":
    import pandas as pd
    df  =  pd.read_csv("album_2022-01-01_2022-01-31.csv")
    get_tracks(df,start=1790,name = "2022-01-01_2022-01-31")
    