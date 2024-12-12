# Copyright 2019 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_pubsub_server]
import base64

from flask import Flask, request

import cv2


app = Flask(__name__)


# [END cloudrun_pubsub_server]
def dummy_function1():
    # read img jpg
    img = cv2.imread("img.jpg")

    # print base64
    print("read successfully")


import os
from typing import Optional
from pytubefix import YouTube
import pytubefix


def download_youtube_video(url: str, output_dir: str = ".") -> None:
    """
    Download a YouTube video in MP4 format.

    Args:
        url (str): The URL of the YouTube video.
        output_dir (str, optional): The directory to save the downloaded video. Defaults to the current directory.
    """
    yt = YouTube(url)

    video = get_highest_resolution_mp4_stream(yt)

    if video:
        print(f"Downloading video: {yt.title}")
        try:
            video.download(output_dir)
            print("Download completed successfully!")
        except Exception as e:
            print(f"Error occurred during download: {e}")
    else:
        print("No MP4 stream found.")


def get_highest_resolution_mp4_stream(yt: YouTube) -> Optional[pytubefix.Stream]:
    """
    Get the highest resolution MP4 stream for the given YouTube object.

    Args:
        yt (YouTube): The YouTube object.

    Returns:
        Optional[pytubefix.Stream]: The highest resolution MP4 stream, or None if not found.
    """
    return (
        yt.streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
    )


def dummy_function3():
    from PIL import Image
    import pytesseract

    img = cv2.imread("img.jpg")
    pytesseract.image_to_string(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))


def dummy_4():
    dummy_function1()
    download_youtube_video("https://www.youtube.com/watch?v=q_zyuPOd3PQ")
    dummy_function3()


# [START cloudrun_pubsub_handler]
@app.route("/", methods=["POST"])
def index():
    """Receive and parse Pub/Sub messages."""
    print("Version 1")
    dummy_4()
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    name = "World"
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        name = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

    print(f"Hello {name}!")

    return ("", 204)


# [END cloudrun_pubsub_handler]


@app.route("/dummy", methods=["POST"])
def dummy():
    dummy_function1()
    download_youtube_video("https://www.youtube.com/watch?v=q_zyuPOd3PQ")
    dummy_function3()
    return ("", 204)
