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

from django_discord.admin import UserAdmin
from django_discord.models import User


class TestUserAdmin(TestCase):
    """Test the model admin for users"""

    def test_username_for_django_admin(self):
        """Verify the model admin is generating column values correctly"""
        user = User(
            id='1234',
            username='user',
            discriminator='1234',
            avatar='',
        )
        user_admin = UserAdmin(user, None)

        self.assertEqual(
            'user#1234',
            user_admin.username_for_django_admin(user)
        )
