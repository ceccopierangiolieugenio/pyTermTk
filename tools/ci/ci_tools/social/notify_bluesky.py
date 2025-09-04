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
import argparse
from datetime import datetime
from pprint import pprint

from typing import Dict

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from social_common import get_social_data, SocialData, get_env_var

import re
from typing import List, Dict

def _parse_mentions(text: str) -> List[Dict]:
    spans = []
    # regex based on: https://atproto.com/specs/handle#handle-identifier-syntax
    mention_regex = rb"[$|\W](@([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)"
    text_bytes = text.encode("UTF-8")
    for m in re.finditer(mention_regex, text_bytes):
        spans.append({
            "start": m.start(1),
            "end": m.end(1),
            "handle": m.group(1)[1:].decode("UTF-8")
        })
    return spans

def _parse_urls(text: str) -> List[Dict]:
    spans = []
    # partial/naive URL regex based on: https://stackoverflow.com/a/3809435
    # tweaked to disallow some training punctuation
    url_regex = rb"[$|\W](https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*[-a-zA-Z0-9@%_\+~#//=])?)"
    text_bytes = text.encode("UTF-8")
    for m in re.finditer(url_regex, text_bytes):
        spans.append({
            "start": m.start(1),
            "end": m.end(1),
            "url": m.group(1).decode("UTF-8"),
        })
    return spans

# Parse facets from text and resolve the handles to DIDs
def _parse_facets(text: str) -> List[Dict]:
    facets = []
    for m in _parse_mentions(text):
        resp = requests.get(
            "https://bsky.social/xrpc/com.atproto.identity.resolveHandle",
            params={"handle": m["handle"]},
        )
        # If the handle can't be resolved, just skip it!
        # It will be rendered as text in the post instead of a link
        if resp.status_code == 400:
            continue
        did = resp.json()["did"]
        facets.append({
            "index": {
                "byteStart": m["start"],
                "byteEnd": m["end"],
            },
            "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}],
        })
    for u in _parse_urls(text):
        facets.append({
            "index": {
                "byteStart": u["start"],
                "byteEnd": u["end"],
            },
            "features": [
                {
                    "$type": "app.bsky.richtext.facet#link",
                    # NOTE: URI ("I") not URL ("L")
                    "uri": u["url"],
                }
            ],
        })
    return facets

def _get_facet(txt:str, slice:str, content:Dict ) -> Dict:
    start = txt.index(slice)
    end = start + len(slice)
    return {
        "index": { "byteStart": start, "byteEnd": end },
        "features": [ content ]
      }


def main():
    parser = argparse.ArgumentParser(description="Send a Discord notification.")
    parser.add_argument("app", type=str, help="The application name.")
    parser.add_argument("version", type=str, help="The application version.")
    args = parser.parse_args()

    data = get_social_data(args.app)
    if not data:
        raise ValueError(f"app: {args.app} is not recognised")

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
    access_token = auth_data["accessJwt"]
    did = auth_data["did"]
    print(f"::add-mask::{did}")
    print(auth_data)

    # Step 2: Post a message
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    text = f"{args.app} v{args.version} Released\n\n{data.link}\n\n#pyTermTk #TUI #Python #Linux #terminal"

    post_data = {
        "repo": did,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text":text,
            "facets": [
                _get_facet(
                    text, data.link,
                    { "uri": data.link , "$type": "app.bsky.richtext.facet#link" }
                ),
                _get_facet(
                    text, '#pyTermTk',
                    { "tag": 'pyTermTk' , "$type": "app.bsky.richtext.facet#tag" }
                ),
                _get_facet(
                    text, '#TUI',
                    { "tag": 'TUI' , "$type": "app.bsky.richtext.facet#tag" }
                ),
                _get_facet(
                    text, '#Python',
                    { "tag": 'Python' , "$type": "app.bsky.richtext.facet#tag" }
                ),
                _get_facet(
                    text, '#Linux',
                    { "tag": 'Linux' , "$type": "app.bsky.richtext.facet#tag" }
                ),
                _get_facet(
                    text, '#terminal',
                    { "tag": 'terminal' , "$type": "app.bsky.richtext.facet#tag" }
                ),
            ],
            "createdAt": datetime.now().isoformat() + "Z"
        }
    }

    print('::group::Data')
    pprint(post_data)
    print('::endgroup::')

    post_response = requests.post(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        headers=headers,
        json=post_data
    )

    print(post_response.status_code)
    print(post_response.json())
if __name__ == "__main__":
    main()