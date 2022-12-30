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