# Authors: Matthew Raaff
# BSD 3-Clause License

import aiohttp
import asyncio
import json

from .novelexception import InvalidToken, NoKeyfile

class APIClient:
    """
    Create a client to interact with a novel instance's API.
    """
    async def __init__(self, base_url, delay=1800):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()
        self.token = None # Wait for the first request to get a token.
        self.delay = delay # Delay in seconds between auto token refreshes.
        self.version = 1 # This client is designed for version 1 of the API.

    """
    Make a raw request to the API.

    @param endpoint: The endpoint to make the request to.
    @param method: The HTTP method to use.
    @param data: The data to send with the request.
    @param headers: The headers to send with the request.
    @return: The response from the server.

    >>> client = NovelClient('http://localhost:15634')
    >>> output = client.make_raw_request('status', method='POST', data={'client': 'py'})
    >>> print(output)

    You should mainly use this method for unimplemented API endpoints, or if you're working on the internal client library.
    """
    async def make_raw_request(self, endpoint, method='GET', data=None, headers=None):
        if headers is None:
            headers = {}
        url = f"{self.base_url}/{endpoint}"
        async with self.session.request(method, url, data=data, headers=headers) as response:
            return await response.text()

    """
    Request a session token from the novel instance.

    @param username: The username to authenticate with.
    @param password: The password to authenticate with.
    @param key: The keyfile in bytes to authenticate with.
    @param autoset: Whether to automatically set the token for the client.
    @return: A session object represented as a dictionary.

    >>> output = client.request_authentication('admin', 'admin')
    >>> client.set_token(output['token'])

    This should only be used at initialisation of the client. The client will automatically request a new token when it expires.
    """
    async def request_authentication(self, username, password, key=None, autoset=True):
        if key is None:
            status = await self.make_raw_request('status')
            status = json.loads(status)
            if status['keyfile_auth']:
                raise NoKeyfile()
        data = {'username': username, 'password': password}
        if key is not None:
            data['key'] = key
        response = await self.make_raw_request('auth', method='POST', data=data)
        response = json.loads(response)
        if autoset:
            self.set_token(response['token'])
        return response

    """
    Set the token for the client.

    @param token: The token to set.
    @return: None

    >>> client.set_token('token')
    """
    def set_token(self, token):
        if token is None:
            raise InvalidToken()
        self.token = token

    """
    Get the token for the client.

    @return: The token for the client.

    >>> token = client.get_token()
    """
    def get_token(self):
        return self.token

    """
    Get the session for the client.

    @return: The session for the client.

    >>> session = client.get_session()
    """
    async def get_session(self):
        if self.token is None:
            raise InvalidToken()
        response = await self.make_raw_request('session', headers={'Authorization': f"Bearer {self.token}"})
        response = json.loads(response)
        return response

    """
    Get the status for the client.

    @return: The status for the client.

    >>> status = client.get_status()
    """
    async def get_status(self):
        response = await self.make_raw_request('status')
        response = json.loads(response)
        return response

    """
    Get a new token for the client.

    @return: The new token for the client.

    >>> token = client.get_new_token()
    """
    async def get_new_token(self):
        response = await self.make_raw_request('auth', method='POST', data={'token': self.token})
        response = json.loads(response)
        self.set_token(response['token'])
        return response

    """
    Schedule a new async task to get a new token every 30 minutes.

    @return: None

    >>> client.schedule_token_refresh()
    """
    def schedule_token_refresh(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._token_refresh())

    """
    Internal method to refresh the token.

    @return: None
    """
    async def _token_refresh(self):
        while True:
            await asyncio.sleep(self.delay)
            await self.get_new_token()

    """
    Get the version of the API client. This is in every client library.

    @return: The version of the API.

    >>> version = client.get_version()
    """
    def get_version(self):
        return self.version

    """
    Close the session for the client.

    @return: None

    >>> client.close()
    """
    async def close(self):
        await self.make_raw_request('logout', method='POST', headers={'Authorization': f"Bearer {self.token}"})
        await self.session.close()