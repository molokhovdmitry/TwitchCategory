import sys
import requests

BASE_URL = 'https://api.twitch.tv/helix/'
CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'
HEADERS = {
    'Authorization': 'Bearer hpc4glg4g2pekdmh5wktio1bsahnp9',
    'Client-Id': CLIENT_ID
}

def getTopGames():
    """
    Get top games.
    
    Return top games dictionary of format:
    {game_id: game_name}
    """

    # Number of objects to return (max: 100)
    first = 100

    # Contact API
    try:
        query = f'games/top?first={first}'
        response = requests.get(BASE_URL + query, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException:
        return None

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
    Returns a list of streams broadcasting a specified game ID.
    """

    # Number of objects to return (max: 100)
    first = 100

    # Contact API
    try:
        query = f'streams?game_id={gameID}&first={first}'
        response = requests.get(BASE_URL + query, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
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