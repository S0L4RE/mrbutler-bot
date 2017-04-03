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

from collections import OrderedDict
from unittest import TestCase
from unittest.mock import patch

from mrb.environment import (
    Environment,
    EnvironmentType,
)


class TestEnvironment(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected_env_length = 2

    def setUp(self):
        patcher = patch('os.getenv')
        self.addCleanup(patcher.stop)
        self.mock_os_getenv = patcher.start()

        self.env = Environment()

    def test_getenv_calls(self):
        """Verify we only are making calls to os.getenv as expected"""
        self.assertEqual(
            self.mock_os_getenv.call_count,
            self.expected_env_length,
        )

    def test_env_vars_ordered_type(self):
        """Ordered environment variables should be an OrderedDict"""
        self.assertIsInstance(self.env.env_vars_ordered, OrderedDict)


class TestEnvironmentHelperMethods(TestCase):
    def test_get_environment_type_dev(self):
        """Standard case, verify that we get a DEV environment"""
        self.assertEqual(
            Environment.get_environment_type('dev'),
            EnvironmentType.DEV,
        )

    def test_get_environment_type_prod(self):
        """Standard case, verify that we get a PROD environment"""
        self.assertEqual(
            Environment.get_environment_type('prod'),
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
            # For each index at it's string value ...
            for idx in range(len(env.value)):
                # Make that character at the index a capital value ...
                lookup_value = capitalize_index(env.value, idx)
                # And use it to lookup the matching EnvironmentType
                self.assertEqual(
                    Environment.get_environment_type(lookup_value),
                    env,
                )

    def test_get_environment_type_invalid(self):
        """Edge case, verify that we get a PROD environment on ValueError"""
        self.assertEqual(
            Environment.get_environment_type('junk data junk data junk data'),
            EnvironmentType.PROD,
        )

    # noinspection PyTypeChecker
    def test_get_environment_type_bad_input_type(self):
        """Edge case, verify that we get PROD from a bad data type"""
        self.assertEqual(
            Environment.get_environment_type(None),
            EnvironmentType.PROD,
        )
        self.assertEqual(
            Environment.get_environment_type(1),
            EnvironmentType.PROD,
        )

    def test_make_log_safe(self):
        """The standard case, verify that the string is made safe"""
        self.assertEqual(
            Environment.make_log_safe('masking your face'),
            '•••••••••••••face',
        )

    def test_make_log_safe_short_strings(self):
        """Edge case, verify that short strings are fully masked"""
        for x in range(1, 8):
            input_token = 'x' * x
            expected = '•' * x

            self.assertEqual(Environment.make_log_safe(input_token), expected)

    def test_make_log_safe_none_type(self):
        """Edge case, verify that a 'None' value is treated as empty string"""
        self.assertEqual(Environment.make_log_safe(None), '')
