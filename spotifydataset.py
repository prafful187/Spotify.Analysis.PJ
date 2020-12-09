import spotipy
import pandas
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "6495a5640a54482c8da4724d037b1ca6"
CLIENT_SECRET = "4565740b54244721a1e4f026aa072cc6"
token = spotipy.oauth2.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
cache_token = token.get_access_token()
sp = spotipy.Spotify(cache_token)
sp.user_playlist_tracks("21lhygv42hmwomcbrhjtpz7da", "5wj6qCBEVvfxjeTbVI0wFA")

def analyze_playlist(creator, playlist_id):
    
    # Create empty dataframe
    playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    # Loop through every track in the playlist, extract features and append the features to the playlist df
    
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    for track in playlist:
        # Create empty dict
        playlist_features = {}
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]
        
        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
        
    return playlist_df

# csv
df.to_csv("dataframe.csv", index = False)
# excel
df.to_excel("dataframe.xlsx", index = False)

# def analyze_playlist_dict(playlist_dict):
    
#     # Loop through every playlist in the dict and analyze it
#     for i, (key, val) in enumerate(playlist_dict.items()):
#         playlist_df = analyze_playlist(*val)
#         # Add a playlist column so that we can see which playlist a track belongs too
#         playlist_df["playlist"] = key
#         # Create or concat df
#         if i == 0:
#             playlist_dict_df = playlist_df
#         else:
#             playlist_dict_df = pd.concat([playlist_dict_df, playlist_df], ignore_index = True)
            
#     return playlist_dict_df
