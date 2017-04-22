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

from mrb_common.commanding import Command


class TestCommand(TestCase):
    def setUp(self):
        self.mock_function = MagicMock()
        self.mock_message = MagicMock(spec=Message)  # type: Message

    def test_exec(self):
        """Verify that calling exec on a command runs the stored function"""
        command = Command(self.mock_function)
        command.execute(self.mock_message)

        self.assertEqual(self.mock_function.call_count, 1)

    def test_exec_called_with_message(self):
        """Verify that calling exec passes a message along to the function"""
        command = Command(self.mock_function)
        command.execute(self.mock_message)

        self.mock_function.assert_called_with(self.mock_message)
