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
This file downloads frames from streams in top categories of twitch.  

Pseudocode:  
    while `Enter` is not pressed:  
        Loop:  
        1) Get top games from twitch api, save them in a database.  
        2) Get a game with a minimum number of saved frames.  
        3) Get logins of streams that are live in that category.  
        4) Download frames from 5 random streams,
        save frame info in the database.
"""

import random
import time
import requests
from threading import Thread
from pathlib import Path
from termcolor import colored

from streamlink import Streamlink

from data.download_functions import download_frames
from data.api import get_top_games, get_streams
from data.db_functions import (session_scope, get_game_count, update_games,
                               min_data_category, max_data_category, add_frame)

from config import DOWNLOAD_PATH, MAX_GAMES

data_path = Path.joinpath(Path(DOWNLOAD_PATH), "frames")


def update_data():
    """Updates data while no input (Enter not pressed)."""
    # Start helper threads.
    input_list = []
    Thread(target=input_thread, args=(input_list, )).start()
    print("Press Enter any time to stop downloading.")

    Thread(target=info_thread, args=(input_list, )).start()

    # Start a streamlink session.
    streamlink_session = Streamlink()

    # Start an api session.
    api_session = requests.session()

    downloaded_streams = 0
    fail_count = 0
    frame_count = 0
    while not input_list:

        # Add games if game limit is not exceeded.
        with session_scope() as db_session:
            game_count = get_game_count(db_session)

        if game_count < MAX_GAMES:

            games = get_top_games(api_session)
            if not games:
                print("Error. Could not get top games.")
                continue
        
            # Update the database with new games.
            with session_scope() as db_session:
                update_games(db_session, games)

        # Get a category with the minimum number of frames.
        with session_scope() as db_session:
            game_id = min_data_category(db_session)[0]

        # Get streams from the category.
        streams = get_streams(api_session, game_id)
        if not streams:
            print("Error. Could not get streams.")
            continue
        
        # Update the category (download frames from 5 streams).
        download_count = 0
        download_attempts = 0
        while streams and download_count < 5 and download_attempts < 10:

            if input_list:
                break

            # Get a random stream.
            stream = random.choice(list(streams))
            streams.discard(stream)

            # Download frames from a stream, update the database.
            print(f"Downloading frames from '{stream}', gameID: {game_id}.")
            download = False
            for frame_path in download_frames(streamlink_session,
                                              stream, game_id):

                # Save a frame in the database.
                with session_scope() as db_session:
                    add_frame(db_session, frame_path, game_id, stream)

                download = True
                frame_count += 1
            
            download_count += download
            download_attempts += 1

            downloaded_streams += download
            fail_count += not download

    print_dataset_info()

    print("Done.")
    print(f"Downloaded {frame_count} frame(s) from {downloaded_streams} "
          f"stream(s). Failed {fail_count} time(s).")


def input_thread(input_list):
    """Thread that waits for an input."""
    input()
    input_list.append(True)
    print(colored("Interrupting. Please wait.", 'green'))


def info_thread(input_list):
    """
    Thread that shows how much data is downloaded and min/max data categories
    every `n` seconds.
    """
    n = 300
    
    print_dataset_info()

    # Repeat every `n` seconds.
    i = 0
    while not input_list:
        if i != n:
            time.sleep(1)
            i += 1
            continue
        i = 0

        print_dataset_info()



def print_dataset_info():
    """Prints dataset info."""
    # Print dataset size.
    print(colored(dir_size(data_path), 'green'))

    # Print the number of games.
    with session_scope() as db_session:
        game_count = get_game_count(db_session)
    print(colored(f"{game_count} game(s)", 'green'))
    
    # Print categories with minumum and maximum number of frames.
    print_min_max()


def dir_size(path):
    """Returns the size of `path` folder."""
    files = list(path.glob('**/*'))
    size = 0
    for file in files:
        if file.is_file():
            size += file.stat().st_size

    # Convert to GB.
    size = size / 1073741824
    
    return "Data size: " + '{:.2f}'.format(size) + " GB"


def print_min_max():
    """Prints categories with minumum and maximum number of frames."""
    with session_scope() as db_session:
        min_category = min_data_category(db_session)
        max_category = max_data_category(db_session)

    if min_category:
        print(colored("Minimum: {} frame(s) in category {}."
                      .format(min_category[1], min_category[0]),
                      'green'))
        print(colored("Maximum: {} frame(s) in category {}."
                      .format(max_category[1], max_category[0]),
                      'green'))


if __name__ == "__main__":
    update_data()
