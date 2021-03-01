"""
This file has functions for requesting:
    1) Top games by amount of viewers.
    2) User names broadcasting a specified game ID.
"""

import sys
import requests

from config import CLIENT_ID, ACCESS_TOKEN

BASE_URL = 'https://api.twitch.tv/helix/'
HEADERS = {
    'Authorization': 'Bearer ' + ACCESS_TOKEN,
    'Client-Id': CLIENT_ID
}

def requestQuery(query):
    """
    Makes a request and returns a response.
    """

    # Contact API
    try:
        response = requests.get(BASE_URL + query, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.RequestException:
        return None

def getTopGames():
    """
    Get top games.
    
    Return top games dictionary of format:
    {game_id: game_name}
    """
    
    # Number of objects to return (100 max)
    first = 100

    # Make query
    query = f'games/top?first={first}'
    response = requestQuery(query)

    # Parse response
    try:
        quote = response.json()
        games = dict()
        for game in quote['data']:
            games[game['id']] = game['name']
        return games
    except (KeyError, TypeError, ValueError):
        return None


def getStreamers(gameID):
    """
    Returns a list of user names broadcasting a specified game ID.
    """

    # Number of objects to return (100 max)
    first = 100

    # Make query
    query = f'streams?game_id={gameID}&first={first}'
    response = requestQuery(query)

    # Parse response
    try:
        quote = response.json()
        streams = list()
        for stream in quote['data']:
            streams.append(stream['user_name'])
        return streams
    except (KeyError, TypeError, ValueError):
        return None

# Debug
#print(getTopGames())
#print(getStreamers('27471'))