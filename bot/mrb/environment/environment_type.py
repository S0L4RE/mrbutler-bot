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

from enum import Enum


class EnvironmentType(Enum):
    """
    Enum for describing environment types
    """

    DEV = 'dev'
    PROD = 'prod'

    @staticmethod
    def get_type(env_input: str=''):
        """
        Determine the environment enum based on a string input

        :param env_input: The string describing the environment
        :return: The 'EnvironmentType' or 'EnvironmentType.PROD' on ValueError
        """
        if not isinstance(env_input, str):
            return EnvironmentType.PROD

        env_input = env_input.lower()

        try:
            result = EnvironmentType(env_input)
        except ValueError:
            result = EnvironmentType.PROD

        return result
