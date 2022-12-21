import requests
from SpotifyAuth import SpotifyAuthorizer
import json
import pandas as pd

#CLIENT_ID and CLIENT_SECRET omitted from version for privacy/security

client = SpotifyAuthorizer(CLIENT_ID, CLIENT_SECRET)
access_token = client.get_access_token()

#billboard top 100 
playlist_id = "6UeSakyzhiEt4NB3UAd6NQ"
playlist_search_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

#header for requests
header = {"Authorization": f"Bearer {access_token}"}

#https://api.spotify.com/v1/search?type=album&include_external=audio
playlist = requests.get(playlist_search_url, headers = header ) 
#convert string dictionary -> normal dictionary
playlist_data = json.loads(playlist.text)

#get urls of every track in the playlist
# and add each track to our pandas DataFrame.

#set columns to wrap data around in dataframe
cols = {'artist_name': [], 'track_name': [], 'danceability': [], 'energy': [], \
'key': [], 'loudness': [], 'mode': [], 'speechiness': [], 'acousticness': [], \
'instrumentalness': [], 'liveness': [], 'valence': [], 'tempo': [], \
'duration_ms': [], 'time_signature': []}

#empty dataframe to add to.
df = pd.DataFrame(cols)

'''
@returns a list of data values for audio features of a track.
@param track_data - general track features
@param audio_data - advanced audio features
'''
def get_track_data(track_data, audio_data):
	#artist name
	artist_info = track_data['album']['artists'][0]
	artist_name = artist_info['name']
	#track name
	track_name = track_data['name'] 
	#storing audio features
	#https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features
	#^ info on each feature
	danceability = audio_data['danceability']
	energy = audio_data['energy']
	key = audio_data['key']
	loudness = audio_data['loudness']
	mode = audio_data['mode']
	speechiness = audio_data['speechiness']
	acousticness = audio_data['acousticness']
	instrumentalness = audio_data['instrumentalness']
	liveness = audio_data['liveness']
	valence = audio_data['valence']
	tempo = audio_data['tempo']
	duration_ms = audio_data['duration_ms']
	time_signature = audio_data['time_signature']

	return [artist_name, track_name, danceability, energy, key, loudness, \
	mode, speechiness, acousticness, instrumentalness, liveness, valence, \
	tempo, duration_ms, time_signature]

#loop to get data for each track in the top 100 billboard(or any playlist)
for index in range(len(playlist_data["tracks"]["items"])):
	#get general features - track name, artist name
	track_url = playlist_data["tracks"]["items"][index]['track']['external_urls']['spotify']
	track_id = track_url.split('/')[-1]
	#setup url and requests
	track_search_url = f"https://api.spotify.com/v1/tracks/{track_id}"
	track = requests.get(track_search_url, headers = header)
	track_data = json.loads(track.text)
	#get the advanced audio features of each track
	audio_search_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
	audio_features = requests.get(audio_search_url, headers = header)
	audio_data = json.loads(audio_features.text)

	track_values = get_track_data(track_data, audio_data)



	#add everything about this track to our dataframe.
	df.loc[len(df.index)] = track_values

#save the DataFrame to a csv for analysis to be done 
df.to_csv('tracks.csv')