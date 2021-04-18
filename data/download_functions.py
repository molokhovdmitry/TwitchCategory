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
This file creates download folders if they don't exist,
has function that downloads frames from stream,
resizes them to required resolution and saves them.  

Functions:  
1) Download stream segments, extract and save frames.  
2) Helper function. Returns the last added frame number for a directory.  
3) Deletes files in `temp` directory.
"""

import requests
import re
from pathlib import Path

import cv2 as cv

from data.log import log

from config import IMG_SIZE, DOWNLOAD_PATH

IMG_HEIGHT = IMG_SIZE["height"]
IMG_WIDTH = IMG_SIZE["width"]

download_path = Path(DOWNLOAD_PATH)
frames_path = Path.joinpath(download_path, "frames")
temp_path = Path.joinpath(download_path, "temp")
data_temp_path = Path.joinpath(temp_path, "data")
recognition_temp_path = Path.joinpath(temp_path, "recognition")
debug_path = Path.joinpath(download_path, "debug")

# Ensure paths exist.
paths = [download_path, frames_path, temp_path, data_temp_path,
         recognition_temp_path, debug_path]
for path in paths:
    if not path.exists():
        path.mkdir()


def download_frames(streamlink_session, login, game_id=None):
    """
    Downloads stream segments in best quality, gets frames from segments,
    resizes frames to required resolution and saves them.  
    
    Saves in `framesPath`/`gameID` folder if `gameID` is passed,
    else saves in `recognitionTempPath`.  
    
    Yields saved frame paths.  
    Returns `None` if can't get frames.
    """
    if game_id:

        # Create `gameID` folder if not exists.
        download_path = Path.joinpath(frames_path, str(game_id))
        if not Path.exists(download_path):
            Path.mkdir(download_path)

        temp_path = data_temp_path
    else:
        download_path = recognition_temp_path
        temp_path = recognition_temp_path

    # Get a dictionary of format {`quality`: `url`} containing 
    # `.m3u8` file urls for every quality.
    try:
        m3u8_links = streamlink_session.streams(f"https://www.twitch.tv/{login}")
    except:
        print(f"Streamlink couldn't get {login}'s stream.")
        return None

    # Ensure the stream is live.
    if not m3u8_links:
        print("Stream not live.")
        return None

    # Get the best quality `.m3u8` url.
    m3u8 = m3u8_links["best"].url
    
    # Request `.m3u8` file.
    response = requests.get(m3u8).text

    # Ensure that `.m3u8` file links to stream source and not to ads.
    if response.lower().count("twitch-ad") > 1:
        print("Ad.")
        return None

    # Get segment links.
    seg_links = re.findall(r'(https?://\S+)', response)[2:-2]

    # Download and save all frames from segments.
    frame_number = last_added_num(download_path) + 1
    for link, seg_number in zip(seg_links, range(1, len(seg_links) + 1)):

        # Request `.ts` file.
        segment = requests.get(link).content

        # Save the file.
        seg_path = Path.joinpath(temp_path, f"segment{seg_number}.ts")
        with open(seg_path, 'wb') as file:
            file.write(segment)

        # Open segment with cv.
        video = cv.VideoCapture(str(seg_path))

        # Ensure it is a video file.
        if not is_video(video):
            video.release()
            seg_path.unlink()
            continue

        try:
            # Get the first frame and release the video.
            frame = video.read()[1]
            video.release()

            # Delete segment.
            seg_path.unlink()

            # Resize and save the frame.
            frame = cv.resize(frame,
                              (IMG_WIDTH, IMG_HEIGHT),
                              interpolation=cv.INTER_AREA)
            frame_path = Path.joinpath(download_path, f"{frame_number}.jpg")
            cv.imwrite(str(frame_path), frame)
            frame_number += 1

            if game_id:
                # Yield path to save it in the database.
                yield  str(Path.joinpath(Path(str(game_id)), frame_path.name))
            else:
                # Yield path for recognition.
                yield str(frame_path)

        except Exception as e:
            print("Unexpected Error.")

            # Save segment in `debugPath`.
            seg_number = last_added_num(debug_path) + 1
            seg_path_debug = Path.joinpath(debug_path, f"{seg_number}.ts")
            with open(seg_path_debug, 'wb') as file:
                file.write(segment)
            print(f"{seg_path_debug.name} saved.")

            # Log data and excepiton.
            log(login, game_id, m3u8_links, m3u8, response, seg_links, e)
            print("Exception saved in data/log.txt.")


def last_added_num(path):
    """
    Returns last added frame number for a `path` directory.
    `path` is a pathlib.Path object.  

    Return 0 if no files in directory.
    """
    files = list(path.iterdir())
    if not files:
        return 0
    
    # Get all frame numbers.
    numbers = [int(str(file.name).split('.')[0]) for file in files]

    return max(numbers)


def is_video(video):
    """
    Checks that `file` is a video file.  

    `video` is cv.VideoCapture object.
    """
    return video.get(cv.CAP_PROP_FRAME_HEIGHT) != 0
