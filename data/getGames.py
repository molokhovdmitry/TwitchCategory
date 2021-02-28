import requests

BASE_URL = 'https://api.twitch.tv/kraken/'
CLIENT_ID = 'mcnhwdta4al9dkgxz543k5cebicpze'
HEADERS = {
    'Client-ID': CLIENT_ID,
    'Accept': 'application/vnd.twitchtv.v5+json'
}

def getTopGames():
    """
    Get top games.
    
    Return a dictionary of top `limit` games.
    """
    limit = 100

    # Contact API
    try:
        query = f'games/top?limit={limit}'
        response = requests.get(BASE_URL + query, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException:
        return "Request Error"

    # Parse response.
    try:
        quote = response.json()
        games = dict()
        for game in quote['top']:
            games[game['game']['_id']] = game['game']['name']
        return games
    except (KeyError, TypeError, ValueError):
        return "Parse Error"

# Debug
print(getTopGames())