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

from .environment_type import EnvironmentType


class Environment(object):
    """
    Class to collect required environment variables for Mr. Butler
    """

    def __init__(self):
        discord_token_key_name = 'MRB_DISCORD_TOKEN'
        mrb_env_key_name = 'MRB_ENV'

        # Configure the internal values for the environment
        self.discord_token = os.getenv(discord_token_key_name)
        self.type = self.get_environment_type(os.getenv(mrb_env_key_name))

        # Configure environment variable collections
        safe_discord_token = self.make_log_safe(self.discord_token)

        self.env_vars_ordered = OrderedDict([
            (discord_token_key_name, safe_discord_token),
            (mrb_env_key_name, self.type),
        ])

        self.env_vars = {}
        for key, value in self.env_vars_ordered.items():
            self.env_vars[key] = value

    @staticmethod
    def get_environment_type(env_input: str= ''):
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

    @staticmethod
    def make_log_safe(token: str=None):
        """
        Given an input token, turn it into a log-safe value.

        This is performed by using a given generic character to mask
        the other values of the token

        :param token: The string to generate a safe instance of
        :return: A string, with all but the last few characters covered up
        """

        if not token:
            token = ''

        safe_char = '•'
        token_length = len(token)
        token_exposed_length = 4
        token_min_length = token_exposed_length * 2

        if token_length >= token_min_length:
            return "{blanks}{last_chars}".format(
                blanks=safe_char * (token_length - token_exposed_length),
                last_chars=token[-token_exposed_length:]
            )
        else:
            return '•' * token_length
