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

import os, sys
import re
import asyncio
import argparse
from typing import Dict,List,Any

import discord

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from social_common import get_social_data, SocialData, get_env_var

async def send_discord_message(version: str, data:SocialData):
    token = get_env_var("DISCORD_TOKEN")
    message = get_env_var("MESSAGE")

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    embed = discord.Embed(
        title=f"{data.name} Released!!!",
        url=data.link,
        # description="Here's a new feature we added.",
        color=0x00ff00,
    )
    embed.add_field(name="Version", value=version, inline=True)
    # embed.add_field(name="What's New:", value=message, inline=False)

    # embed.set_image(url="https://example.com/image.png")
    # embed.add_field(name="Feature", value="Auto-messaging", inline=False)
    embed.set_footer(text="Bot by Pier...")
    message = re.sub(r'\((https?://[^\)]+)\)', r'(<\1>)', message).replace('\\n','\n')[:2000]
    # print(message)
    # exit(1)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        channel = client.get_channel(data.discord_channel_id)
        await channel.send(embed=embed)
        await channel.send(message)
        await client.close()  # Optional: close after sending

    await client.start(token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a Discord notification.")
    parser.add_argument("app", type=str, help="The application name.")
    parser.add_argument("version", type=str, help="The application version.")
    args = parser.parse_args()

    data = get_social_data(args.app)
    if not data:
        raise ValueError(f"app: {args.app} is not recognised")

    asyncio.run(send_discord_message(args.version, data))