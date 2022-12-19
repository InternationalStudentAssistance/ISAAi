# Copyright (C) 2022 ISAAi contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import getpass

import aiohttp
import aiohttp.web
import keyring


def create_handler(password, page_id):
    async def handler(request: aiohttp.web.Request):
        data = await request.post()
        content = data["body-plain"]

        await add_to_notion_page(password, page_id, content)

        return aiohttp.web.Response(text="OK")

    return handler


async def add_to_notion_page(password, page_id, content):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"

        headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "Authorization": f"Bearer {password}",
        }

        payload = {
            "children": [
                {
                    "object": "block",
                    "parent": {"type": "page_id", "page_id": page_id},
                    "has_children": False,
                    "archived": False,
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": content,
                                },
                            }
                        ],
                        "color": "default",
                        "children": [],
                    },
                }
            ]
        }

        async with session.patch(url, json=payload, headers=headers) as resp:
            print(resp.status)
            json = await resp.json()

            try:
                print(json["message"])
            except KeyError:
                pass


def main():
    password = keyring.get_password("Notion", "SimonBiggs")

    if not password:
        password = getpass.getpass()
        keyring.set_password("Notion", "SimonBiggs", password)

    page_id = "ad816892782d478d9998f700a5c783be"
    handler = create_handler(password, page_id)

    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.post("/", handler)])
    aiohttp.web.run_app(app)
