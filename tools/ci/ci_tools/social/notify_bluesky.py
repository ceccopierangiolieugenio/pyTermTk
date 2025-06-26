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
import requests
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from social_common import get_social_data, SocialData, get_env_var

identifier=get_env_var('BLUESKY_APP_IDENTIFIER')
password=get_env_var('BLUESKY_APP_PWD')

# Step 1: Authenticate and get access token
auth_response = requests.post(
    "https://bsky.social/xrpc/com.atproto.server.createSession",
    headers = {
        "Content-Type": "application/json"
    },
    json={
        "identifier": identifier,
        "password": password
    }
)

auth_data = auth_response.json()
# print(auth_data)
access_token = auth_data["accessJwt"]
did = auth_data["did"]

# Step 2: Post a message
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

post_data = {
    "repo": did,
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": "Hello from my Python bot!",
        "createdAt": datetime.now().isoformat() + "Z"
    }
}

post_response = requests.post(
    "https://bsky.social/xrpc/com.atproto.repo.createRecord",
    headers=headers,
    json=post_data
)

print(post_response.status_code)
print(post_response.json())
