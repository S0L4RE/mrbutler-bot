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

from rest_framework import serializers

from django_discord.models import (
    Guild,
    User,
)


class GuildSerializer(serializers.ModelSerializer):
    """Serializer for Discord Guilds"""

    class Meta:
        model = Guild

        fields = (
            'id',
            'created_ts',
            'updated_ts',
        )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Discord Users"""

    class Meta:
        model = User

        fields = (
            'id',
            'created_ts',
            'updated_ts',
        )
