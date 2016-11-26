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

from django.test import TestCase

from django_discord.models import User


class TestUserModel(TestCase):
    """Test the Discord User model in Django"""

    def test_snowflake_id(self):
        """Test the 64bit (uint64) string id"""

        expected_id = '18446744073709551615'
        discord_user = User.objects.create(id=expected_id)

        self.assertEqual(discord_user.id, expected_id)
        self.assertIsInstance(discord_user.id, str)

    def test_str(self):
        """Test the __str__ representation"""

        user_id = '18446744073709551615'
        user_name = 'SomeUser'
        user_discriminator = '1234'
        expected_str = "Discord User <{0}#{1} -- {2}>".format(
            user_name,
            user_discriminator,
            user_id,
        )
        discord_user = User.objects.create(
            id=user_id,
            discriminator=user_discriminator,
            username=user_name,
        )

        self.assertEqual(str(discord_user), expected_str)
