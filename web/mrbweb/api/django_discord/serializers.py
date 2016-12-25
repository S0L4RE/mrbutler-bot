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
            'name',
            'owner',
            'icon',
            'created_ts',
            'updated_ts',
        )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Discord Users"""

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        action = self.context['view'].action

        if action in ['update', 'partial_update']:
            kwargs = extra_kwargs.get('id', {})
            kwargs['read_only'] = True
            extra_kwargs['id'] = kwargs

        return extra_kwargs

    class Meta:
        model = User

        fields = (
            'id',
            'username',
            'discriminator',
            'avatar',
            'created_ts',
            'updated_ts',
        )
