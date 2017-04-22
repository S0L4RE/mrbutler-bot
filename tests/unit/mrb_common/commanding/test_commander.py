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
from unittest.mock import MagicMock

from discord import Message

from mrb_common.commanding import Commander


class TestCommander(TestCase):
    def setUp(self):
        self.commander = Commander()

    def test_add(self):
        """Verify commands can be added"""
        self.commander.add('test', MagicMock())
        self.assertEqual(len(self.commander._commands), 1)

    def test_add_duplicate(self):
        """Verify a KeyError is raised when adding a duplicate command"""
        self.commander.add('test', MagicMock())
        with self.assertRaises(KeyError):
            self.commander.add('test', MagicMock())

    def test_execute(self):
        """Verify commands can be executed"""
        mock_function = MagicMock()
        self.commander.add('test', mock_function)
        self.commander.execute('test', MagicMock(spec=Message))
        self.assertEqual(mock_function.call_count, 1)

    def test_execute_undefined(self):
        """Verify no-op occurs when an undefined command is executed"""
        self.commander.execute('test', MagicMock(spec=Message))

    def test_remove(self):
        """Verify commands can be removed"""
        self.commander.add('test', MagicMock())
        self.commander.remove('test')
        self.assertEqual(len(self.commander._commands), 0)

    def test_remove_undefined(self):
        """Verify a KeyError is raised when removing an undefined command"""
        with self.assertRaises(KeyError):
            self.commander.remove('test')
