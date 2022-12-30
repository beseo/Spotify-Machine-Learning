# Spotify-Machine-Learning
Using Spotify's REST API to gather data, and analyze and predict with the gathered data.
# <b>Spotify Billboard Music Analysis</b>

The overall goal of the project:

 - Gather data on every single track in Spotify's Top 100 Billboard playlist <i>(as of November 23, 2022)</i> using Spotify's REST API and the requests module in Python.

 - Create visualizations using Seaborn and Plotly and perform analysis with the data that I find. 
 
 - Make educated predictions through the use of Scikit to answer the question: "What makes a hit song?"

This github page covers the <b>first half</b> of this project, which involves <b>gathering the data</b>.<br><br>
The <b>second half</b> of this project may be seen on my <b>Kaggle notebook</b>, which covers <b>data wrangling, analysis, visualization, and machine learning</b>: <b>[Link] (https://www.kaggle.com/code/beomsukseo/spotify-billboard-analysis)</b>
 
# <b>Preparation to Gather the Data</b>

To gather the data required for this project, I first created a 'SpotifyAPI' class that using the requests and base64 Python modules (*the client credentials for the Spotify API requires base64 encoding*):

```Python
import base64   #for Spotify's base64 encoding
import requests #to call Spotify's REST API

class SpotifyAPI():
    
    access_token = None
    client_id = None
    client_secret = None
    
    #constructor for when we create an instance of this class
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://accounts.spotify.com/api/token"

    # returns the base64 encoded client credientials 
    # using a client's ID and 'secret' value, obtained
    # through Spotify's REST API.
    def get_client_creds(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("Client ID and/or Client Secret Missing.")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_base64 = base64.b64encode(client_creds.encode())
        return client_creds_base64.decode()
    
    # returns header needed to make a request
    # to Spotify's REST server.
    # return format: <base64 encoded client_id:client_secret>
    def get_token_header(self):
        return {
            "Authorization" : f"Basic {self.get_client_creds()}", 
            "Content-Type": "application/x-www-form-urlencoded"
        }

    # returns the data (access grant type) needed to
    # make a request to Spotify's server.
    def get_token_data(self):
        return {"grant_type": "client_credentials"}
    
    # uses other methods defined above to make a request  
    # to Spotify's API, and returns the access token from
    # the json response.  
    def get_access_token(self):
        r = requests.post(self.token_url, data= self.get_token_data(), headers = self.get_token_header())
        token_response = r.json()
        return token_response['access_token']
```
# <b>Gathering the Data - Billboard Top 100</b>

Using access token recieved from the SpotifyAPI class, we will make a series of requests to receive information about each track in the playlist (Billboard Top 100): the track's name, duration, danceability, and other calculations that Spotify has available. 

Beggining with our imports, the modules: Requests, Json, and Pandas will be used for this section:
```Python
import requests       #making calls to the API
import json           #formatting code output so it's more readable 
import pandas as pd   #making of a DataFrame that we convert to a CSV later on, to store our data.
```
Next, I created an instance of the SpotifyAPI class, and used the get_access_token() method defined above to generate my personal access token to access Spotify's database. I then store the link for a playlist (in our case, Billboard 100) to reach Spotify's API server. Note the 'header' variable I define in the format of Spotify's API documentation, which we will input as a parameter for when we use the requests module. 
```Python
# NOTE: my personal CLIENT_ID and CLIENT_SECRET have been defined in a separate, private code cell for privacy reasons.

# construct an instance of the SpotifyAPI class defined earlier 
client = SpotifyAPI(CLIENT_ID, CLIENT_SECRET)

#calling of the method get_access_token() on our object 
access_token = client.get_access_token()

# this playlist_id is the link Spotify uses for their Billboard 100 playlist.
# this id can be changed to any other playlist ID.
playlist_id = "6UeSakyzhiEt4NB3UAd6NQ"
playlist_search_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

#header for requests *(This is Spotify's specific format)
header = {"Authorization": f"Bearer {access_token}"}
```
<b>Receiving All the Data in the Chosen Playlist</b>

To get the playlist data, we use the requests module, inputting the playlist search URL as well as the headers we defined above as parameters. The json module will also be used to format the requests response.

In addition, we eventually want a Pandas DataFrame to store all our datapoints, so we will create an empty DataFrame to begin with, and have the columns all labeled in order.

```Python
playlist = requests.get(playlist_search_url, headers = header) 

# string dictionary -> normal dictionary
playlist_data = json.loads(playlist.text)

#set columns to wrap data around in dataframe
cols = {'artist_name': [], 'track_name': [], 'danceability': [], 'energy': [], \
'key': [], 'loudness': [], 'mode': [], 'speechiness': [], 'acousticness': [], \
'instrumentalness': [], 'liveness': [], 'valence': [], 'tempo': [], \
'duration_ms': [], 'time_signature': []}

#empty dataframe to add to, using columns defined above.
df = pd.DataFrame(cols)
```

<font size = 4><b>Formatting our data to fit into our table:</b>

We will be running a loop through the playlist_data we found above, and for every track we will separately look up its specific audio data. With this, we must format them into our Pandas DataFrame automatically.

The method get_track_data() returns a list of all the formatted track's data points, in the same order as our DataFrame defined above (it's really just an easy way to format all our data into our DataFrame). </font>
```Python
#returns a list of data values for audio features of a track.
#param track_data - general track features
#param audio_data - advanced audio features
def get_track_data(track_data, audio_data):
    #artist name
    artist_info = track_data['album']['artists'][0]
    artist_name = artist_info['name']
    
    #track name
    track_name = track_data['name'] 
    
    #storing audio features
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
    
    #return in order of our DataFrame.
    return [artist_name, track_name, danceability, energy, key, loudness, \
    mode, speechiness, acousticness, instrumentalness, liveness, valence, \
    tempo, duration_ms, time_signature]
```
<font size = 4><b>Iterating Through the Playlist</b>

Now to actually go through our specified playlist, we loop over the length of the amount of tracks in the playlist. For each iteration, we get all the data we can about the track from Spotify's REST database, then call our get_track_data() method to format the data, and finally insert it into our DataFrame (<i>The inline comments will explain in more detail if you're interested</i>).</font>

```Python
for index in range(len(playlist_data["tracks"]["items"])):
    #get track_id to look up specific track on the database.
    track_url = playlist_data["tracks"]["items"][index]['track']['external_urls']['spotify']
    track_id = track_url.split('/')[-1]
    
    # get general track feature of current track
    track_search_url = f"https://api.spotify.com/v1/tracks/{track_id}"
    track = requests.get(track_search_url, headers = header)
    track_data = json.loads(track.text)
    # get advanced audio features of current track
    audio_search_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    audio_features = requests.get(audio_search_url, headers = header)
    audio_data = json.loads(audio_features.text)
    
    # call the method get_track_data() and store the returned list of data for this track, in order.
    track_values = get_track_data(track_data, audio_data)

    # add the list of data (in-order) for this track into our dataframe at the next available row.
    df.loc[len(df.index)] = track_values
```
Finally, we can export our Pandas DataFrame as a .csv file so we can use our newly found data in the next section of the project. If you've made it this far, thank you! As a reminder, the next and final part of this project is available on my Kaggle notebook <a href = "https://www.kaggle.com/code/beomsukseo/spotify-billboard-analysis"><b>here.</b></a>
```Python
df.to_csv('tracks.csv')
```
