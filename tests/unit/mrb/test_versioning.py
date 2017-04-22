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

from discord import (
    Message,
    User,
)

from mrb import versioning
from mrb_common.commanding import (
    CommandResult,
    ResponseType,
)


class TestGetVersion(TestCase):
    def test_type(self):
        """Verify that a type of string is returned"""
        self.assertIsInstance(versioning.get_version(), str)

    def test_non_zero_length(self):
        """Verify that a non-zero length string is returned"""
        self.assertGreater(len(versioning.get_version()), 0)


class TestGetVersionCommand(TestCase):
    def setUp(self):
        self.user = User(
            name='TestUser',
            id='TestUserId',
            discriminator='0000',
            avatar='',
            bot=False,
        )

        self.mock_message = MagicMock(spec=Message)  # type: Message
        self.mock_message.author = self.user

    def test_type(self):
        """Verify that the correct result type is returned"""
        self.assertIsInstance(
            versioning.get_version_command(self.mock_message),
            CommandResult,
        )

    def test_response_content_user_mention(self):
        """Verify that the version command mentions the user"""
        self.assertIn(
            self.user.mention,
            versioning.get_version_command(self.mock_message).content,
        )

    def test_response_content_version_value(self):
        """Verify that the version command contains the version"""
        self.assertIn(
            versioning.get_version(),
            versioning.get_version_command(self.mock_message).content,
        )

    def test_response_success(self):
        """Verify that the response is always successful"""
        self.assertTrue(
            versioning.get_version_command(self.mock_message).success
        )

    def test_response_type(self):
        """Verify that the version command is a channel response type"""
        self.assertEqual(
            versioning.get_version_command(self.mock_message).response_type,
            ResponseType.ChannelMessage,
        )
