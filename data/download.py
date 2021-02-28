import streamlink
from subprocess import Popen
from time import sleep
import sys

stream_url = streamlink.streams("https://www.twitch.tv/vadikus007")["best"].url

ffmpeg_process = Popen(["ffmpeg", "-i", stream_url, "-c", "copy", "stream.mkv"])

sleep(5)

ffmpeg_process.kill()
