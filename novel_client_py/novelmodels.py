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