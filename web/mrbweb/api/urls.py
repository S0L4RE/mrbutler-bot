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

from django.conf.urls import (
    include,
    url,
)
from rest_framework import routers

from .django_discord.views import (
    GuildViewSet,
    UserViewSet,
)

router = routers.DefaultRouter()


router.register(r'discord/guilds', GuildViewSet)
router.register(r'discord/users', UserViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
