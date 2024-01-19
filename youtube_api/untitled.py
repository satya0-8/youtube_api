def get_channel_stats(youtube,channel_ids):
    
    all_data=[]
    
    request=youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )
    
    response=request.execute()
    
    for i in response['items']:
        data={'channelName': i['snippet']['title'],
              'subscribers': i['statistics']['subscriberCount'],
              'views': i['statistics']['viewCount'],
        'totalVideos': i['statistics']['videoCount'],
        'playlistId': i['contentDetails']['relatedPlaylists']['uploads']
        }
        all_data.append(data)
    return(pd.DataFrame(all_data))
def get_video_ids(youtube,playlist_id):
    
    video_ids=[]
    
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    
    response = request.execute()
    
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
    
    next_page_token=response.get('nextPageToken')
    
    while next_page_token is not None:
        request = youtube.playlistItems().list(part="contentDetails",
                  playlistId=playlist_id,
                  maxResults=50,
                  pageToken=next_page_token)
        
        response = request.execute()
        
        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])
        
        next_page_token=response.get('nextPageToken')
        
    return video_ids
