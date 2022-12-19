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

import getpass
import keyring
import asyncio

import aiohttp
import aiohttp.web


def create_handler(password):
    async def handler(request: aiohttp.web.Request):
        data = await request.post()
        
        print(data)

    return handler



async def get_notion_page(password, page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "Authorization": f"Bearer {password}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            print(resp.status)
            print(await resp.text())



def main():
    password = keyring.get_password("Notion", "SimonBiggs")

    if not password:
        password = getpass.getpass()
        keyring.set_password("Notion", "SimonBiggs", password)

    asyncio.run(get_notion_page(password, 'ad816892782d478d9998f700a5c783be'))

    handler = create_handler(password)

    app = aiohttp.web.Application()
    app.add_routes([aiohttp.web.post('/', handler)])
    aiohttp.web.run_app(app)
