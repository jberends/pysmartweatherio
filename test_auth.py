#!/bin/env python3

import asyncio
import aiohttp

from pysmartweatherio.authentication import Auth, AbstractAuth

async def main():

   async with aiohttp.ClientSession() as session: 
       auth = Auth(session, "http://example.com/api", "secret_access_token")


if __name__ == '__main__':
    asyncio.run(main())