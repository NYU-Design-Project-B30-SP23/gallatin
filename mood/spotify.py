'''
This is the main file for the application. This application will
create playlists for specific moods for a certain user using their own music.
The user can either manually input their mood or the program will use a facial
recognition API to detect the mood of the user by taking a picture of them
after they have provided the program with all user scopes required. The program
uses machine learning on a training set created using Last.fm tags and features
about the songs obtained through Spotify to create the playlist for the user to
try and classify the user's music into specific moods. 

In order to run the application, you must supply your unique user ID as the
second argument in the terminal. Example:python spotify.py userID 
This file defines the user scopes and prompts a user for their token 
in order to access their data. The program will run until the user manually
quits the program using 1. 
'''
#Load libraries
import sys
import json
import spotipy
import spotipy.util as util
import os
import createPlaylist
import getTrainingData
import learnSongs

CLIENT_ID = 'ce931c51bc334b5288daa5e5ba897d5a'
CLIENT_SECRET = '26fb987dce6d4294ae77d5da59ab2a73'

# id: 563f890f0bc540309c44d40e35a0a462
# secret: 343030b9e9d0440b80bebb96647485af

#Tries to obtain username from terminal
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Please supply a user ID")
    username = input("Your choice: ")
    # sys.exit()

scopes = ("user-read-recently-played"
          " user-top-read"
          " user-library-modify"
          " user-library-read"
          " user-read-private"
          " playlist-read-private"
          " playlist-modify-public"
          " playlist-modify-private"
          " user-read-email"
          " user-read-private"
          " user-read-playback-state"
          " user-modify-playback-state"
          " user-read-currently-playing"
          " app-remote-control"
          " streaming"
          " user-follow-read"
          " user-follow-modify")

#prompt for user permission
# try:
#     token = util.prompt_for_user_token(username,scopes,
#                                    client_id=CLIENT_ID,
#                                    client_secret=CLIENT_SECRET,
#                                    redirect_uri='http://google.com/')
# except:
#     os.remove(".cache-{}".format(username))
#     token = util.prompt_for_user_token(username,scopes,
#                                    client_id=CLIENT_ID,
#                                    client_secret=CLIENT_SECRET,
#                                    redirect_uri='http://google.com/')
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes,
                                                  client_id=CLIENT_ID,
                                                  client_secret=CLIENT_SECRET,
                                                  redirect_uri='http://google.com/',
                                                  username=username,
                                                  open_browser=False))
token = 1
if token:
    #define spotify object and user
    # sp = spotipy.Spotify(auth=token)
    # sp = spotipy.Spotify(auth_manager=token)
    user = sp.current_user()

    #will run till user quits the program
    print("Welcome to the Sentiment Recommender! Please choose an option.")
    print("0-Create personalized playlist")
    print("1-exit")
    print("")

    #user can manually input mood
    print("If you would like to manually input a mood, please enter happy, angry, sad, or relaxed. Else just click enter.")
    choice =  input("Your choice: ")
    if choice != '':
        mood = choice
    else:
        mood = "sad"
    model = learnSongs.main()
    createPlaylist.main(sp, user, model, mood)
    print("Successfully created playlist!")
    #End program

