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

from unittest import TestCase

from mrb.environment import EnvironmentType


class TestEnvironmentType(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected_env_type_length = 2

    def test_known_environments_available(self):
        """Given known environment types, verify we have a matching Enum"""
        known_envs = [
            'dev',
            'prod',
        ]

        for known_env in known_envs:
            env_enum = EnvironmentType(known_env)

            self.assertEqual(
                known_env,
                env_enum.value,
            )

    def test_known_environment_length(self):
        """Verify that we have a known number of environments at all times"""
        known_environments = list(EnvironmentType.__members__.items())

        self.assertEqual(
            self.expected_env_type_length,
            len(known_environments),
        )


class TestEnvironmentTypeHelperMethods(TestCase):
    def test_get_environment_type_dev(self):
        """Standard case, verify that we get a DEV environment"""
        self.assertEqual(
            EnvironmentType.get_type('dev'),
            EnvironmentType.DEV,
        )

    def test_get_environment_type_prod(self):
        """Standard case, verify that we get a PROD environment"""
        self.assertEqual(
            EnvironmentType.get_type('prod'),
            EnvironmentType.PROD,
        )

    def test_get_environment_type_uppercase(self):
        """Edge case, verify that we get proper environments with uppercase"""

        def capitalize_index(value: str, index: int):
            """
            Given an input string, capitalize a letter at a given index.

            :param value: The string that will have a capitalized letter
            :param index: The index at which to perform the capitalizing
            :return: The string, with a letter capitalized at a given index
            """
            return value[:index] + value[index:].capitalize()

        # For each known environment ...
        for env in EnvironmentType:
            # For each index at its string value ...
            for idx in range(len(env.value)):
                # Make that character at the index a capital value ...
                lookup_value = capitalize_index(env.value, idx)
                # And use it to lookup the matching EnvironmentType!
                self.assertEqual(
                    EnvironmentType.get_type(lookup_value),
                    env,
                )

    def test_get_environment_type_invalid(self):
        """Edge case, verify that we get a PROD environment on ValueError"""
        self.assertEqual(
            EnvironmentType.get_type('junk data junk data'),
            EnvironmentType.PROD,
        )

    # noinspection PyTypeChecker
    def test_get_environment_type_bad_input_type(self):
        """Edge case, verify that we get PROD from a bad data type"""
        self.assertEqual(
            EnvironmentType.get_type(None),
            EnvironmentType.PROD,
        )
        self.assertEqual(
            EnvironmentType.get_type(1),
            EnvironmentType.PROD,
        )
