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