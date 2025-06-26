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
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from social_common import get_social_data, SocialData, get_env_var


# === CONFIGURATION ===
GITHUB_TOKEN = get_env_var('GH_DISCUSSION_TOKEN')
REPO_OWNER = "ceccopierangiolieugenio"
REPO_NAME = "pyTermTk"
DICSUSSION_CATEGORY="announcements"
DISCUSSION_TITLE = "Your Announcement Title"
DISCUSSION_BODY = "This is the content of your announcement."

# === FUNCTIONS ===

def get_repo_id(owner, repo, token):
    query = f"""
    query {{
      repository(owner: "{owner}", name: "{repo}") {{
        id
      }}
    }}
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    return response.json()['data']['repository']['id']

def get_category_id(repo_id, token):
    query = f"""
    query {{
      node(id: "{repo_id}") {{
        ... on Repository {{
          discussionCategories(first: 10) {{
            nodes {{
              id
              name
            }}
          }}
        }}
      }}
    }}
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    categories = response.json()['data']['node']['discussionCategories']['nodes']
    for category in categories:
        if category['name'].lower() == DICSUSSION_CATEGORY:
            return category['id']
    raise Exception("Announcements category not found")

def create_discussion(repo_id, category_id, title, body, token):
    mutation = f"""
    mutation {{
      createDiscussion(input: {{
        repositoryId: "{repo_id}",
        categoryId: "{category_id}",
        title: "{title}",
        body: "{body}"
      }}) {{
        discussion {{
          id
          url
        }}
      }}
    }}
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post('https://api.github.com/graphql', json={'query': mutation}, headers=headers)
    data = response.json()
    print("DEBUG: Create Discussion response:", data)  # Add this line
    return data['data']['createDiscussion']['discussion']['url']

# === MAIN EXECUTION ===

try:
    repo_id = get_repo_id(REPO_OWNER, REPO_NAME, GITHUB_TOKEN)
    print(f"{repo_id=}")
    category_id = get_category_id(repo_id, GITHUB_TOKEN)
    print(f"{category_id=}")
    discussion_url = create_discussion(repo_id, category_id, DISCUSSION_TITLE, DISCUSSION_BODY, GITHUB_TOKEN)
    print(f"{discussion_url=}")
    print(f"✅ Discussion created successfully: {discussion_url}")
except Exception as e:
    print(f"❌ Error: {e}")
