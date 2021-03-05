"""
This file downloads stream segments and saves frames.

Functions:
1) Download stream segments, ensure they're not an ad.
2) Get frames from a segment and save them in filesystem and database.
"""

import streamlink
import requests
from subprocess import Popen
from time import sleep
import sys
import re


def downloadStream(login):
    """
    Download stream segments in 480p quality.
    
    Returns `None` if gets an ad.
    """

    """
    Get a dictionary of format {`quality`: `url`} containing `.m3u8` file urls for every quality.
    """

    links = streamlink.streams(f"https://www.twitch.tv/{login}")

    # Get stream qualities
    qualities = [quality for quality in links]

    if "480p" not in qualities:
        print("No 480p")
        return None
    # Get 480p `.m3u8` url
    m3u8 = links["480p"].url
    
    # Get `.m3u8` file
    response = requests.get(m3u8).text
    # Ensure that `.m3u8` file links to stream source and not to ads
    if response.lower().count("twitch-ad") > 1:
        print("Ad")
        return None
    else:
        # Get segment links
        links = re.findall(r'(https?://\S+)', response)[1:-2]

        # Download and save all segments
        for link, i in zip(links, range(1, len(links) + 1)):
            # Request `.ts` file
            segment = requests.get(link).content

            # Save file
            name = f"segment{i}.ts"
            with open(name, 'wb') as f:
                f.write(segment)


def saveFrames(segment):
    raise NotImplementedError