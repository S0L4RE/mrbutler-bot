"""
Copyright 2017 Peter Urda

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
from typing import Optional

from .environment_type import EnvironmentType


class Environment(object):
    """
    Class to collect required environment variables for Mr. Butler
    """

    _DISCORD_TOKEN_KEY_NAME = 'MRB_DISCORD_TOKEN'
    _MRB_ENV_KEY_NAME = 'MRB_ENV'

    def __init__(self):
        # Configure the internal values for the environment
        self._discord_token = os.getenv(self._DISCORD_TOKEN_KEY_NAME)
        self._discord_token_safe = None
        self._type = self._get_mrb_env(os.getenv(self._MRB_ENV_KEY_NAME))

        # Configure a "safe" string that we can log for the 'discord_token'
        if self._discord_token and len(self._discord_token) > 4:
            self._discord_token_safe = "{blanks}{last_chars}".format(
                blanks='•'*(len(self._discord_token) - 4),
                last_chars=self._discord_token[-4:],
            )

        self._env_vars_ordered = OrderedDict([
            (self._DISCORD_TOKEN_KEY_NAME, self._discord_token_safe),
            (self._MRB_ENV_KEY_NAME, self.type),
        ])

    @staticmethod
    def _get_mrb_env(env_input: str=''):
        """
        Determine the environment enum based on a string input

        :param env_input: The string describing the environment
        :return: The 'EnvironmentType' or 'EnvironmentType.PROD' on ValueError
        """
        try:
            result = EnvironmentType(env_input)
        except ValueError:
            result = EnvironmentType.PROD

        return result

    @property
    def discord_token(self) -> Optional[str]:
        """
        The determined API token for Discord.
        :return: The API token as a string, or None if unset.
        """
        return self._discord_token

    @property
    def env_vars_ordered(self) -> OrderedDict:
        """
        Convenience property to get an ordered dictionary
        of all environment settings
        """
        return self._env_vars_ordered

    @property
    def type(self) -> EnvironmentType:
        """
        The determined EnvironmentType for this Environment
        :return: The loaded EnvironmentType, or EnvironmentType.PROD if unset.
        """
        return self._type
