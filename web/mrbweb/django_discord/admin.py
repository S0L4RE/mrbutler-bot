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

from django.contrib import admin

from .models import (
    Guild,
    User,
)


class AdminMixins(admin.ModelAdmin):
    """
    Common Mixin class for some Django Discord ModelAdmins
    """

    def get_readonly_fields(self, request, obj=None):
        """
        Many Django Discord Models have 'id' fields that should not be changed
        after an object has been created.
        """
        if obj:
            return self.readonly_fields + ['id']

        return self.readonly_fields


class GuildAdmin(AdminMixins):
    """Admin options for the User model"""

    fieldsets = [
        ('Guild Data', {
            'fields': [
                'id',
                'name',
                'owner',
                'icon',
            ],
        }),
        ('Metadata', {
            'fields': [
                'created_ts',
                'updated_ts',
            ],
        }),
    ]

    list_display = (
        'name',
        'id',
    )

    list_filter = [
        'created_ts',
        'updated_ts',
    ]

    raw_id_fields = [
        'owner',
    ]

    readonly_fields = [
        'created_ts',
        'updated_ts',
    ]

    search_fields = [
        'id',
        'name',
        'owner__id',
        'owner__username',
    ]


class UserAdmin(AdminMixins):
    """Admin options for the User model"""

    def username_for_django_admin(self, user) -> str:
        return user.full_discord_username

    username_for_django_admin.short_description = 'User'

    fieldsets = [
        ('User Data', {
            'fields': [
                'id',
                'username',
                'discriminator',
                'avatar',
            ],
        }),
        ('Metadata', {
            'fields': [
                'created_ts',
                'updated_ts',
            ],
        }),
    ]

    list_display = (
        'username_for_django_admin',
        'id',
    )

    list_filter = [
        'created_ts',
        'updated_ts',
    ]

    readonly_fields = [
        'created_ts',
        'updated_ts',
    ]

    search_fields = [
        'id',
        'username',
        'discriminator',
    ]


admin.site.register(Guild, GuildAdmin)
admin.site.register(User, UserAdmin)
