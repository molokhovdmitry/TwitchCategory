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

downloadPath = Path(DOWNLOAD_PATH)
framesPath = Path.joinpath(downloadPath, "frames")
tempPath = Path.joinpath(downloadPath, "temp")
dataTempPath = Path.joinpath(tempPath, "data")
recognitionTempPath = Path.joinpath(tempPath, "recognition")
debugPath = Path.joinpath(downloadPath, "debug")

"""Ensure paths exist."""
paths = [downloadPath, framesPath, tempPath, dataTempPath,
         recognitionTempPath, debugPath]
for path in paths:
    if not path.exists():
        path.mkdir()


def downloadFrames(streamlinkSession, login, gameID=None):
    """
    Downloads stream segments in best quality, gets frames from segments,
    resizes frames to required resolution and saves them.
    
    Saves in `framesPath`/`gameID` folder if `gameID` is passed,
    else saves in `recognitionTempPath`.
    
    Yields saved frame paths.
    Returns `None` if can't get frames.
    """

    if gameID:
        """Create `gameID` folder if not exists."""
        downloadPath = Path.joinpath(framesPath, str(gameID))
        tempPath = dataTempPath
        if not Path.exists(downloadPath):
            Path.mkdir(downloadPath)
    else:
        downloadPath = recognitionTempPath
        tempPath = recognitionTempPath
    
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

        """Open segment with cv."""
        video = cv.VideoCapture(str(segmentPath))

        """Ensure it is a video file."""
        if not isVideo(video):
            video.release()
            segmentPath.unlink()
            continue

        try:
            """Get the first frame and release the video."""
            frame = video.read()[1]
            video.release()

            """Delete segment."""
            segmentPath.unlink()

            """Resize and save the frame."""
            frame = cv.resize(frame,
                              (IMG_WIDTH, IMG_HEIGHT),
                              interpolation=cv.INTER_AREA)
            framePath = Path.joinpath(downloadPath, f"{frameNumber}.jpg")
            cv.imwrite(str(framePath), frame)
            frameNumber += 1

            if gameID:
                """Yield path to save it in the database."""
                yield  str(Path.joinpath(Path(str(gameID)), framePath.name))
            else:
                """Yield path for recognition."""
                yield str(framePath)
        
        except Exception as e:
            print("Unexpected Error.")
            num = lastAddedNum(debugPath) + 1
            segmentPathDebug = Path.joinpath(debugPath, f"{num}.ts")
            with open(segmentPathDebug, 'wb') as file:
                file.write(segment)
            print(f"{segmentPathDebug.name} saved.")
            log(login, gameID, m3u8Links, m3u8, response, segLinks, e)
            print("Exception saved in data/log.txt.")


def lastAddedNum(path):
    """
    Returns last added frame number for a `path` directory.
    `path` is a pathlib.Path object.

    Return 0 if no files in directory.
    """

    files = list(path.iterdir())
    if not files:
        return 0
    
    """Get all frame numbers."""
    numbers = [int(str(file.name).split('.')[0]) for file in files]

    return max(numbers)


def isVideo(video):
    """
    Checks that `file` is a video file.

    `video` is cv.VideoCapture object.
    """

    return video.get(cv.CAP_PROP_FRAME_HEIGHT) != 0
