"""
This file creates download folders if they don't exist,
has function that downloads frames from stream,
resizes them to required resolution and saves them.

Functions:
1) Download stream segments, ensure they're not an ad.
2) Get frames from a segment and save them in filesystem and database.
"""

import streamlink
import requests
import re
import os
import cv2 as cv
import pathlib

"""Saved image resolution."""
IMG_HEIGHT = 480
IMG_WIDTH = 854

"""Create required folders if not exist."""
from config import DOWNLOAD_PATH

downloadPath = DOWNLOAD_PATH
framesPath = downloadPath + f"frames{os.sep}"
tempPath = downloadPath + f"temp{os.sep}"

"""Ensure paths exist."""
if not os.path.exists(downloadPath):
    os.mkdir(downloadPath)
if not os.path.exists(framesPath):
    os.mkdir(framesPath)
if not os.path.exists(tempPath):
    os.mkdir(tempPath)

def downloadFrames(login, gameID=None):
    """
    Download stream segments in best quality, get frames from segments,
    resize frames to required resolution and save them.
    
    Saves in `framesPath`/`gameID` folder if `gameID` is passed,
    else saves in `framesPath`/`temp`.
    
    Yields saved frame paths.
    Returns `None` if gets an ad.
    """

    if gameID:
        """Create `gameID` folder if not exists."""
        downloadPath = f"{framesPath}{gameID}{os.sep}"
        if not os.path.exists(downloadPath):
            os.mkdir(downloadPath)
    else:
        downloadPath = tempPath
    
    """
    Get a dictionary of format {`quality`: `url`} containing 
    `.m3u8` file urls for every quality.
    """
    try:
        links = streamlink.streams(f"https://www.twitch.tv/{login}")
    except:
        print("Error. Streamlink couldn't get the stream.")
        return None

    """Get the best quality `.m3u8` url."""
    if not links:
        print("Streamer not live.")
        return None
    m3u8 = links["best"].url
    
    """Get `.m3u8` file."""
    response = requests.get(m3u8).text
    """Ensure that `.m3u8` file links to stream source and not to ads."""
    if response.lower().count("twitch-ad") > 1:
        print("Ad.")
        return None

    """Get segment links."""
    links = re.findall(r'(https?://\S+)', response)[2:-2]

    """Download and save all frames from segments."""
    frameNumber = lastAddedNum(downloadPath) + 1
    for link, i in zip(links, range(1, len(links) + 1)):

        """Request `.ts` file."""
        segment = requests.get(link).content

        """Save file."""
        segmentPath = f"{tempPath}segment{i}.ts"
        with open(segmentPath, 'wb') as f:
            f.write(segment)

        try:
            """Open segment with cv."""
            video = cv.VideoCapture(segmentPath)

            """Get first frame and release video."""
            frame = video.read()[1]
            video.release()

            """Resize frame and save."""
            frame = cv.resize(frame, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv.INTER_AREA)
            framePath = f"{downloadPath}{frameNumber}.jpg"
            cv.imwrite(framePath, frame)
            frameNumber += 1
            
            if gameID:
                """Yield path for saving in the database."""
                yield f"{gameID}{os.sep}{os.path.basename(framePath)}"
            else:
                """Yield path for recognition."""
                yield framePath

        except:
            print("Error. Couldn't get a frame from segment.")

        finally:
            """Delete segment."""
            os.remove(segmentPath)
    
    print("Downloaded frames.")


def lastAddedNum(downloadPath):
    """
    Return last added frame number for a `downloadPath` directory.

    Return 0 if no files in directory.
    """

    files = os.listdir(downloadPath)
    if not files:
        return 0
    
    """Get all frame numbers and return max."""
    numbers = [int(file.rstrip('.jpg')) for file in files]
    return max(numbers)


def delTempFiles():
    """Delete files in `tempPath`."""
    
    path = pathlib.Path(tempPath)
    for file in list(path.glob("*")):
        file.unlink()
