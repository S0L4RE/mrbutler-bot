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

from django.db import models

from .mixins import CreatedUpdatedFieldsMixin


class User(
    CreatedUpdatedFieldsMixin,
    models.Model
):
    """
    Django model to represent a Discord User

    https://discordapp.com/developers/docs/resources/user
    """

    id = models.CharField(
        primary_key=True,
        max_length=20,
        help_text='The snowflake ID of this user from Discord'
    )

    username = models.CharField(
        max_length=32,
        help_text='The username for this user',
    )

    discriminator = models.CharField(
        max_length=4,
        help_text='The 4-digit discord-tag for this user',
    )

    avatar = models.CharField(
        max_length=255,
        help_text="The user's avatar hash",
    )

    is_bot = models.BooleanField(
        'Bot User',
        help_text='Is this Discord user a bot?',
    )

    def __str__(self):
        return "{0.full_discord_username} - {0.id}".format(self)

    @property
    def full_discord_username(self) -> str:
        """
        Get the user#tag string for this User

        :return: A string formatted as 'username#discriminator'
        """

        return "{0.username}#{0.discriminator}".format(self)
