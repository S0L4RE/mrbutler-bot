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

from letsencrypt.models import AcmeChallenge
from rest_framework import serializers


class AcmeChallengeSerializer(serializers.ModelSerializer):
    acme_url = serializers.SerializerMethodField()

    # noinspection PyMethodMayBeStatic
    def get_acme_url(self, obj):
        """DRF method to get the access the Acme URL from the object"""
        return obj.get_acme_url()

    class Meta:
        model = AcmeChallenge

        fields = (
            'id',
            'challenge',
            'response',
            'acme_url',
            'created_ts',
            'updated_ts',
        )
