"""
Copyright 2016 Peter Urda

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from collections import OrderedDict


class Environment(object):
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
