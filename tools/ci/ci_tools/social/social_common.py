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
# SOFTWARE.from dataclasses import dataclass

__all__ = ['get_social_data','SocialData','get_env_var']

import os
from dataclasses import dataclass
from typing import List

@dataclass
class SocialData():
    name: str
    link: str
    image: str
    discord_channel_id: int

_all_data:List[SocialData] = [
        SocialData(
            name='pytermtk',
            link='https://github.com/ceccopierangiolieugenio/pyTermTk',
            image='',
            discord_channel_id=1379381341145268305,
        ),
        SocialData(
            name='ttkode',
            link='https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/apps/ttkode',
            image='',
            discord_channel_id=1379381474783924295,
        ),
        SocialData(
            name='thedumbpainttool',
            link='https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/apps/dumbPaintTool',
            image='',
            discord_channel_id=1379381571412430931,
        ),
        SocialData(
            name='tlogg',
            link='https://github.com/ceccopierangiolieugenio/pyTermTk/tree/main/apps/tlogg',
            image='',
            discord_channel_id=1379381593378000916,
        ),
]

def get_social_data(app:str) -> SocialData:
    for _sd in _all_data:
        if _sd.name.lower() == app.lower():
            return _sd
    raise ValueError(f"app: {app} is not recognised")

def get_env_var(name:str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise EnvironmentError(f"{name} environment variable is not available")
    return value