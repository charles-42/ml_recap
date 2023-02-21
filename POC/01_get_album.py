def get_album_by_date(start,end):
    import musicbrainzngs
    import pandas as pd
    musicbrainzngs.set_useragent(
        "plus-de-gout",
        "0.1"
    )

    df = pd.DataFrame(columns=["title","status","date","country","tag_list","artist_name"])

    query = f"date:[{start}T00:00:00 TO {end}T23:59:59] AND type:album"
    limit = musicbrainzngs.search_releases(query=query,limit=1)
    print(limit["release-count"])
    for i in range(0,limit["release-count"],100):
        my_request = musicbrainzngs.search_releases(date='2022',type="album",limit=100, offset = i)
    
        for j in range(0,len(my_request['release-list'])):
            title = my_request['release-list'][j].get("title")
            status = my_request['release-list'][j].get("status")
            date =   my_request['release-list'][j].get("date")
            country =   my_request['release-list'][j].get("country")
            tag_list = my_request['release-list'][j].get('tag-list')
            if my_request['release-list'][j].get('artist-credit'):
                artist_name =  my_request['release-list'][j].get('artist-credit')[0].get('name')
            else:
                artist_name = None
            
            list_row = [title,status,date,country,tag_list,artist_name]
            df.iloc[len(df)] = list_row
        print(i)
    df["tag_list"] = df["tag_list"].apply(lambda x : [tag.get('name') for tag in eval(x)])
    df.to_csv(f"album_{start}_{end}.csv")
    

if __name__ == "__main__":
    start  = "2022-01-01"
    end = "2022-01-31"
    get_album_by_date(start,end)