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

from mrb_core.environment_type import EnvironmentType


class Environment(object):
    """
    Class to collect required environment variables for Mr. Butler
    """

    _DISCORD_ADMIN_ID_KEY_NAME = 'MRB_ADMIN_ID'
    _DISCORD_TOKEN_KEY_NAME = 'MRB_DISCORD_TOKEN'
    _MRB_ENV_KEY_NAME = 'MRB_ENV'

    def __init__(self):
        self._stashed_env_vars_ordered = None

        self.discord_admin_id = os.getenv(
            self._DISCORD_ADMIN_ID_KEY_NAME,
            None,
        )

        self.discord_token = os.getenv(
            self._DISCORD_TOKEN_KEY_NAME,
            None,
        )

        self.type = self._get_mrb_env(
            os.getenv(
                self._MRB_ENV_KEY_NAME,
                'prod',
            )
        )

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
    def env_vars_ordered(self) -> OrderedDict:
        """
        Convenience property to get an ordered dictionary
        of all environment settings
        """

        if self._stashed_env_vars_ordered is None:
            self._stashed_env_vars_ordered = OrderedDict([
                (self._DISCORD_ADMIN_ID_KEY_NAME, self.discord_admin_id),
                (self._DISCORD_TOKEN_KEY_NAME, self.discord_token),
                (self._MRB_ENV_KEY_NAME, self.type),
            ])

        return self._stashed_env_vars_ordered
