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

from config import IMG_SIZE
from config import DOWNLOAD_PATH

IMG_HEIGHT = IMG_SIZE["height"]
IMG_WIDTH = IMG_SIZE["width"]

downloadPath = Path(DOWNLOAD_PATH)
framesPath = Path.joinpath(downloadPath, "frames")
tempPath = Path.joinpath(downloadPath, "temp")

"""Ensure paths exist."""
if not Path.exists(downloadPath):
    Path.mkdir(downloadPath)
if not Path.exists(framesPath):
    Path.mkdir(framesPath)
if not Path.exists(tempPath):
    Path.mkdir(tempPath)


def downloadFrames(streamlinkSession, login, gameID=None):
    """
    Download stream segments in best quality, get frames from segments,
    resize frames to required resolution and save them.
    
    Saves in `framesPath`/`gameID` folder if `gameID` is passed,
    else saves in `framesPath`/`temp`.
    
    Yields saved frame paths.
    Returns `None` if can't get frames.
    """

    if gameID:
        """Create `gameID` folder if not exists."""
        downloadPath = Path.joinpath(framesPath, str(gameID))
        if not Path.exists(downloadPath):
            Path.mkdir(downloadPath)
    else:
        downloadPath = tempPath
    
    """
    Get a dictionary of format {`quality`: `url`} containing 
    `.m3u8` file urls for every quality.
    """
    try:
        m3u8Links = streamlinkSession.streams(f"https://www.twitch.tv/{login}")
    except:
        print(f"Streamlink couldn't get {login}'s stream.")
        return None

    """Ensure the stream is live."""
    if not m3u8Links:
        print("Stream not live.")
        return None
    
    """Get the best quality `.m3u8` url."""
    m3u8 = m3u8Links["best"].url
    
    """Request `.m3u8` file."""
    response = requests.get(m3u8).text
    
    """Ensure that `.m3u8` file links to stream source and not to ads."""
    if response.lower().count("twitch-ad") > 1:
        print("Ad.")
        return None

    """Get segment links."""
    segLinks = re.findall(r'(https?://\S+)', response)[2:-2]

    """Download and save all frames from segments."""
    frameNumber = lastAddedNum(downloadPath) + 1
    for link, i in zip(segLinks, range(1, len(segLinks) + 1)):

        """Request `.ts` file."""
        segment = requests.get(link).content

        """Save the file."""
        segmentPath = Path.joinpath(tempPath, f"segment{i}.ts")
        with open(segmentPath, 'wb') as file:
            file.write(segment)

        try:
            """Open segment with cv."""
            video = cv.VideoCapture(str(segmentPath))

            """Get the first frame and release the video."""
            frame = video.read()[1]
            video.release()

            """Resize and save the frame."""
            frame = cv.resize(frame,
                              (IMG_WIDTH, IMG_HEIGHT),
                              interpolation=cv.INTER_AREA)
            framePath = Path.joinpath(downloadPath, f"{frameNumber}.jpg")
            cv.imwrite(str(framePath), frame)
            frameNumber += 1
            
            if gameID:
                """Yield path for saving in the database."""
                yield  str(Path.joinpath(Path(str(gameID)), framePath.name))
            else:
                """Yield path for recognition."""
                yield str(framePath)

        except:
            print("Error. Couldn't get a frame from segment.")

        finally:
            """Delete segment."""
            segmentPath.unlink()
    
    print("Frames downloaded.")


def lastAddedNum(path):
    """
    Return last added frame number for a `path` directory.
    `path` is a pathlib.Path object.

    Return 0 if no files in directory.
    """

    files = list(path.iterdir())
    if not files:
        return 0
    
    """Get all frame numbers and return max."""
    numbers = [int(str(file.name).rstrip('.jpg')) for file in files]
    return max(numbers)


def delTempFiles():
    """Delete files in `tempPath`."""
    
    for file in list(tempPath.iterdir()):
        file.unlink()
