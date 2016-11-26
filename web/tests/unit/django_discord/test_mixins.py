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

from django_discord.mixins import AdminMixins
from django_discord.models import User


class TestAdminMixins(TestCase):
    """Test some Admin Mixin behaviors"""

    def test_existing_user_readonly_fields(self):
        """Using the User model, test if 'id' is on an existing object"""
        sample_mixin = AdminMixins(User, None)
        sample_mixin.readonly_fields = []
        self.assertIn('id', sample_mixin.get_readonly_fields(None, True))

    def test_new_user_readonly_fields(self):
        """Using the User model, test if 'id' is not on a new object"""
        sample_mixin = AdminMixins(User, None)
        sample_mixin.readonly_fields = []
        self.assertNotIn('id', sample_mixin.get_readonly_fields(None, None))
