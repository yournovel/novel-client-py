import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json

class NovelUser():
    """
    Represents a user on a novel instance.

    @param client: The client to use for requests.
    @param username: The username of the user.
    @param token: The token of the user.
    @param id: The ID of the user.
    """
    def __init__(self, client, username, token, id):
        self.client = client
        self.username = username
        self.token = token
        self.id = id

        self.key = None
        self.iv = None

    """
    Get the user's profile.

    @return: The user's profile.
    """
    async def get_profile(self):
        return await self.client.make_request(f"users/{self.id}/profile", token=self.token)

    """
    Get the user's entries.

    @param page: The page of entries to get.
    @param limit: The amount of entries to get.
    @return: The user's entries.
    """
    async def get_entries(self, page=1, limit=10):
        return await self.client.make_request(f"users/{self.id}/posts?page={page}&limit={limit}", token=self.token)

    """
    Decrypt an entry locally.

    @param entry: The entry to decrypt.
    @return: The decrypted entry in UltraMD.
    """
    async def decrypt_entry(self, entry):
        x = await self.client.make_request(f"users/{self.id}/posts/{entry['id']}", token=self.token)
        x = json.loads(x)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = unpad(cipher.decrypt(base64.b64decode(x['content'])), AES.block_size)
        return decrypted.decode('utf-8')