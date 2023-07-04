import sys
import spotipy
import spotipy.util as util
import os
import createPlaylist
import learnSongs
import python_weather
import asyncio
import os
from python_weather.enums import Kind
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "418d3d088ba34fcf925e30167643f1a0"
CLIENT_SECRET = "eb365dbf1cfb43efa902bdaf8ada9463"

async def getweather(location):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(location)
    return weather

def get_mood(weather):
    temp = weather.current.feels_like
    match weather.current.kind:
        case Kind.SUNNY | Kind.PARTLY_CLOUDY:  # case 1
            if temp < 0:
                mood = "sad"
            elif temp < 10:
                mood = "happy"
            elif temp < 20:
                mood = "relaxed"
            elif temp < 30:
                mood = "happy"
            else:
                mood = "angry"
        case Kind.CLOUDY | Kind.VERY_CLOUDY:  # case 2
            if temp < 0:
                mood = "sad"
            elif temp < 30:
                mood = "relaxed"
            else:
                mood = "angry"
        case Kind.FOG:  # case 3
            if temp < 10:
                mood = "sad"
            elif temp < 30:
                mood = "relaxed"
            else:
                mood = "angry"
        case Kind.LIGHT_SHOWERS | Kind.LIGHT_SLEET_SHOWERS | Kind.LIGHT_SNOW | Kind.LIGHT_RAIN | Kind.HEAVY_SHOWERS:  # case 4
            if temp < 0:
                mood = "sad"
            elif temp < 10:
                mood = "happy"
            elif temp < 30:
                mood = "relaxed"
            else:
                mood = "angry"
        case Kind.LIGHT_SLEET | Kind.THUNDERY_SHOWERS | Kind.THUNDERY_HEAVY_RAIN | Kind.THUNDERY_SNOW_SHOWERS:  # case 5
            mood = "angry"
        case Kind.HEAVY_SNOW | Kind.HEAVY_RAIN:  # case 6
            if temp < 0:
                mood = "sad"
            elif temp < 10:
                mood = "angry"
            elif temp < 30:
                mood = "relaxed"
            else:
                mood = "angry"
        case Kind.LIGHT_SNOW_SHOWERS | Kind.HEAVY_SNOW_SHOWERS:  # case 7
            if temp < 30:
                mood = "sad"
            else:
                mood = "angry"
        case _:  # default case
            mood = "happy"
    return mood

def auth(username):
    # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    # for more details

    scopes = (
        "user-read-recently-played"
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
        " user-follow-modify"
    )

    try:
        token = util.prompt_for_user_token(username,scopes,
									client_id=CLIENT_ID,
									client_secret=CLIENT_SECRET,
									redirect_uri='http://google.com/')
    except:
        os.remove(".cache-{}".format(username))
        token = util.prompt_for_user_token(username,scopes,
									client_id=CLIENT_ID,
									client_secret=CLIENT_SECRET,
									redirect_uri='http://google.com/')
        
    return token

def generate_playlist(token, city, mood, count, usermode):
    
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    weather = asyncio.run(getweather(city))
    if mood == "random":
        mood = get_mood(weather)
    try:
        size = int(count)
    except:
        print("Count is not a intger: ", count)
        size = 1
    mode = usermode
    sp = spotipy.Spotify(auth=token)
    user = sp.current_user()
    model = learnSongs.main()
    
    try:
        createPlaylist.main(sp, user, model, mood, size, mode)
        return True
    except Exception:
        return False
