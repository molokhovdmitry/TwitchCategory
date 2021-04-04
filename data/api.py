"""
MIT License

Copyright (c) 2021 molokhovdmitry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
This file has functions that get data from twitch api.

Functions:
    1) Request helper function.
    2) Get top games by amount of viewers.
    3) Get user logins that broadcast a specified game ID.
    4) Get game name from game ID.
"""

import requests

from config import CLIENT_ID, ACCESS_TOKEN

BASE_URL = 'https://api.twitch.tv/helix/'
HEADERS = {
    'Authorization': 'Bearer ' + ACCESS_TOKEN,
    'Client-Id': CLIENT_ID
}

def requestQuery(session, query, payload):
    """Make a request and return a response."""

    """Contact API."""
    try:
        response = session.get(BASE_URL + query,
                               params=payload,
                               headers=HEADERS)
        response.raise_for_status()

        return response

    except requests.RequestException:
        return None

def getTopGames(session):
    """
    Return top games dictionary of format:
    {game_id: game_name}
    """

    notVideoGames = {
        "509658": "Just Chatting",
        "26936": "Music",
        "509660": "Art",
        "518203": "Sports",
        "417752": "Talk Shows & Podcasts",
        "509670": "Science & Technology",
        "66082": "Games + Demos",
        "5899": "Stocks And Bonds",
        "743": "Chess",
        "369418": "GeoGuessr",
        "27284": "Retro",
        "509659": "ASMR",
        "488190": "Poker",
        "498566": "Slots"
    }
    
    """Number of objects to return (100 max)."""
    first = 45

    """Make a query."""
    query = f'games/top'
    payload = {'first': first}

    """Make a request."""
    response = requestQuery(session, query, payload)
    if not response:
        print("getTopGames error. No response from API.")
        return None

    """Parse the response."""
    try:
        quote = response.json()
        games = dict()
        for game in quote['data']:
            
            id = game['id']
            name = game['name']

            """Ensure it's a video game."""
            if id in notVideoGames:
                continue

            """Ensure the game is streamed by more than 90 streamers."""
            if len(getStreams(session, id)) > 90:
                games[id] = name

        return games

    except (KeyError, TypeError, ValueError):
        print("getTopGames error. Can't parse the response.")
        return None


def getStreams(session, gameID):
    """Return a set of user logins that broadcast a specified game ID."""

    """Number of objects to return (100 max)."""
    first = 100

    """Make a query."""
    query = f"streams"
    payload = {'game_id': gameID, 'first': first}

    """Make a request."""
    response = requestQuery(session, query, payload)
    if not response:
        print(f"getStreams error. No response from API. Game ID: {gameID}")
        return None
    
    """Parse the response."""
    try:
        quote = response.json()
        streams = set()
        for stream in quote['data']:
            streams.add(stream['user_login'])

        return streams

    except (KeyError, TypeError, ValueError):
        print(f"getStreams error. Can't parse the response. Game ID: {gameID}")
        return None
    

def gameIDtoName(session, gameID):
    """Converts game ID to name using the API."""

    """Make a query."""
    query = f"games"
    payload = {'id': gameID}

    """Make a request."""
    response = requestQuery(session, query, payload)
    if not response:
        print(f"gameIDtoName error. No response from API. Game ID: {gameID}")
        return None

    """Parse the response."""
    try:
        quote = response.json()
        game = quote['data'][0]['name']

        return game

    except (KeyError, TypeError, ValueError):
        print(f"gameIDtoName error. Can't parse the response. Game ID: {gameID}")
        return None
