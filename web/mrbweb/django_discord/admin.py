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

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Admin options for the User model"""

    fieldsets = [
        ('User Data', {
            'fields': [
                'id',
            ],
        }),
        ('Metadata', {
            'fields': [
                'created_ts',
                'updated_ts',
            ],
        }),
    ]

    readonly_fields = [
        'created_ts',
        'updated_ts',
    ]


admin.site.register(User, UserAdmin)
