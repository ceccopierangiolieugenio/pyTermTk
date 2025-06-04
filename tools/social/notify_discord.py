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

import os
import asyncio
import argparse

import discord

def _get_env_var(name:str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise EnvironmentError(f"{name} environment variable is not available")
    return value

async def send_discord_message(channel_id: int):
    token = _get_env_var("DISCORD_TOKEN")
    message = _get_env_var("MESSAGE")

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        channel = client.get_channel(channel_id)
        await channel.send(message)
        await client.close()  # Optional: close after sending

    await client.start(token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send a Discord notification.")
    parser.add_argument("app", type=str, help="The application name.")
    args = parser.parse_args()

    channel_id:int = {
        'pytermtk' : 1379381341145268305,
        'ttkode' : 1379381474783924295,
        'dumbpainttool' : 1379381571412430931,
        'tlogg' : 1379381593378000916,
    }.get(args.app.lower(),0)
    if not channel_id:
        raise ValueError(f"app: {args.app} is not recognised")

    asyncio.run(send_discord_message(channel_id))