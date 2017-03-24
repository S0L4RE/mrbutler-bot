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
        known_environments = list(EnvironmentType.__members__.items())

        self.assertEqual(
            self.expected_env_type_length,
            len(known_environments),
        )
