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
import cv2

"""Saved image resolution."""
IMG_HEIGHT = 480
IMG_WIDTH = 854

"""Create required folders if not exist."""
from config import DOWNLOAD_PATH

downloadPath = DOWNLOAD_PATH
framesPath = downloadPath + f"{os.sep}frames{os.sep}"
tempPath = downloadPath + f"{os.sep}temp{os.sep}"

"""Ensure paths exist."""
if not os.path.exists(downloadPath):
    os.mkdir(downloadPath)
if not os.path.exists(framesPath):
    os.mkdir(framesPath)
if not os.path.exists(tempPath):
    os.mkdir(tempPath)

def downloadFrames(login, gameID):
    """
    Download stream segments in best quality, get frames from segments,
    resize frames to required resolution and save them in `gameID` folder.
    
    Yield saved frame paths.
    Returns `None` if gets an ad.
    """

    """Create `gameID` folder if not exists."""
    gamePath = f"{framesPath}{gameID}{os.sep}"
    if not os.path.exists(gamePath):
        os.mkdir(gamePath)

    """
    Get a dictionary of format {`quality`: `url`} containing 
    `.m3u8` file urls for every quality.
    """
    links = streamlink.streams(f"https://www.twitch.tv/{login}")

    """Get best quality `.m3u8` url."""
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
    frameNumber = lastAddedNum(gameID) + 1
    for link, i in zip(links, range(1, len(links) + 1)):
        """Request `.ts` file."""
        segment = requests.get(link).content

        """Save file."""
        segmentPath = f"{tempPath}segment{i}.ts"
        with open(segmentPath, 'wb') as f:
            f.write(segment)

        """Open segment with cv2."""
        video = cv2.VideoCapture(segmentPath)

        """Get first frame."""
        frame = video.read()[1]

        """Resize frame and save."""
        frame = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_AREA)
        framePath = f"{gamePath}{frameNumber}.jpg"
        cv2.imwrite(framePath, frame)
        frameNumber += 1

        """Delete segment."""
        os.remove(segmentPath)

        """Yield path to save in database."""
        yield f"{gameID}{os.sep}{os.path.basename(framePath)}"
    
    print("Downloaded frames.")


def lastAddedNum(gameID):
    """
    Return last added frame number for a `gameID` folder.

    Return 0 if no files in folder.
    """

    gamePath = f"{framesPath}{gameID}{os.sep}"
    files = os.listdir(gamePath)
    if not files:
        return 0
    
    """Get all frame numbers and return max."""
    numbers = [int(file.rstrip('.jpg')) for file in files]
    return max(numbers)
