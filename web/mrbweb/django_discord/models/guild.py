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
from .user import User


class Guild(
    CreatedUpdatedFieldsMixin,
    models.Model
):
    """
    Django model to represent a Discord Guild (Server)

    https://discordapp.com/developers/docs/resources/guild
    """

    id = models.CharField(
        primary_key=True,
        max_length=20,
        help_text='The snowflake ID of this guild from Discord'
    )

    name = models.CharField(
        max_length=100,
        help_text='The name for this guild',
    )

    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='servers',
        help_text="The user that owns this guild",
    )

    icon = models.CharField(
        max_length=255,
        help_text="The guild's icon hash value",
    )

    members = models.ManyToManyField(
        User,
        related_name='guilds',
        related_query_name='guild',
    )

    def __str__(self):
        return "Discord Guild <{0} - {1}>".format(
            self.id,
            self.name,
        )
