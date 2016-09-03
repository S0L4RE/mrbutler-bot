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

from collections import OrderedDict
from unittest import TestCase
from unittest.mock import patch

from mrb import Environment


class TestEnvironment(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = Environment()
        cls.expected_env_length = 2

    def test_admin_id(self):
        self.assertEqual(
            self.env._DISCORD_ADMIN_ID_KEY_NAME,
            'MRB_ADMIN_ID',
        )

    def test_token_key(self):
        self.assertEqual(
            self.env._DISCORD_TOKEN_KEY_NAME,
            'MRB_DISCORD_TOKEN',
        )

    @patch('os.getenv')
    def test_getenv_calls(self, os_getenv_patched):
        os_getenv_patched.return_value = None
        _ = Environment()
        self.assertEqual(
            os_getenv_patched.call_count,
            self.expected_env_length,
        )

    def test_environment_property_length(self):
        self.assertEqual(len(self.env.environment), self.expected_env_length)

    def test_environment_property_type(self):
        actual = self.env.environment
        expected = OrderedDict

        self.assertIsInstance(
            actual,
            expected,
            msg="Expected a {0}, instead got a {1}".format(
                expected,
                type(actual),
            )
        )
