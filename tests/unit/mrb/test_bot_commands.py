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

from logging import Logger
from unittest import TestCase
from unittest.mock import (
    call,
    patch,
    MagicMock,
)

from discord import Message

from mrb import BotCommands


class TestBotCommands(TestCase):
    def setUp(self):
        self.mock_logger = MagicMock(spec=Logger)  # type: Logger
        self.mock_message = MagicMock(spec=Message)  # type: Message
        self.bot_commands = BotCommands(logger=self.mock_logger)

    def test_configure_commands(self):
        """Verify that commands are configured through the parent's add"""
        mock_add = MagicMock()
        raw_input = {}
        expected_calls = []

        for x in range(3):
            call_trigger = 'trigger{0}'.format(x)
            call_command = 'command{0}'.format(x)
            call_help = 'help_text{0}'.format(x)

            raw_input[call_trigger] = (call_command, call_help)
            expected_calls.append(call(
                trigger=call_trigger,
                command=call_command,
                help_text=call_help,
            ))

        self.bot_commands.add = mock_add
        self.bot_commands.configure_commands(raw_input)

        # We allow any_order here since configure_commands is working with
        # a dict, and the order will not always be the same
        mock_add.assert_has_calls(expected_calls, any_order=True)

    def test_execute_raises_error(self):
        """Verify that calling execute raises an expected exception"""
        with self.assertRaises(NotImplementedError):
            self.bot_commands.execute('', self.mock_message)

    def test_logger_defined(self):
        """Verify the logger is attached to the object"""
        self.assertEqual(self.bot_commands._logger, self.mock_logger)

    @patch('mrb_common.commanding.commander.Commander.execute')
    def test_parse_message(self, mock_super_execute):
        """
        Verify that parsing calls the parent object with a token and message

        :type mock_super_execute: MagicMock
        """
        token = '!token'
        content = 'content'
        self.mock_message.content = '{0} {1}'.format(token, content)

        self.bot_commands.parse_message(self.mock_message)

        mock_super_execute.assert_called_with(token, self.mock_message)
