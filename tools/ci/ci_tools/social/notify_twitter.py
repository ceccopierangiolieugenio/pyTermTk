#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2025 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os,sys
import json
import requests
import argparse
from requests_oauthlib import OAuth1Session


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from social_common import get_social_data, SocialData, get_env_var

def send_twitter_message(version: str, data:SocialData, text:str):
    api_key = get_env_var("X_API_KEY")
    api_secret = get_env_var("X_API_SECRET")
    access_token = get_env_var("X_ACCESS_TOKEN")
    access_token_secret = get_env_var("X_ACCESS_TOKEN_SECRET")

    twitter = OAuth1Session(api_key, api_secret, access_token, access_token_secret)

    payload = {"text": text}
    response = twitter.post("https://api.twitter.com/2/tweets", json=payload)

    print(response.status_code)
    print(response.json())

def main():
    parser = argparse.ArgumentParser(description="Send a Twitter/X notification.")
    parser.add_argument("app", type=str, help="The application name.")
    parser.add_argument("version", type=str, help="The application version.")
    args = parser.parse_args()

    data = get_social_data(args.app)
    if not data:
        raise ValueError(f"app: {args.app} is not recognised")

    text = f"{args.app} v{args.version} Released\n\n{data.link}\n\n#pyTermTk #TUI #Python #Linux #terminal"
    send_twitter_message(args.version, data, text)

if __name__ == "__main__":
    main()