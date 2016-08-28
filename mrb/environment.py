import os
from collections import OrderedDict


class MrbEnvironment(object):
    _DISCORD_ADMIN_ID_KEY_NAME = 'MRB_ADMIN_ID'
    _DISCORD_TOKEN_KEY_NAME = 'MRB_DISCORD_TOKEN'

    def __init__(self):
        self.DiscordAdminId = os.getenv(self._DISCORD_ADMIN_ID_KEY_NAME, None)
        self.DiscordToken = os.getenv(self._DISCORD_TOKEN_KEY_NAME, None)

    @property
    def environment(self) -> OrderedDict:
        return OrderedDict([
            (self._DISCORD_ADMIN_ID_KEY_NAME, self.DiscordAdminId),
            (self._DISCORD_TOKEN_KEY_NAME, self.DiscordToken),
        ])
