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


class Guild(models.Model):
    """
    Django model to represent a Discord Guild (Server)

    https://discordapp.com/developers/docs/resources/guild
    """

    id = models.CharField(
        primary_key=True,
        max_length=20,
        help_text='The snowflake ID of this guild from Discord'
    )

    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Discord Guild <{}>".format(self.id)