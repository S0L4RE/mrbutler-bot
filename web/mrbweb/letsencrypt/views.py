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

from django.http import (
    HttpResponse,
    HttpResponseNotFound,
)


def detail(request, acme_data):
    _ = request  # noqa
    expected_request = 'lX8D7FNGoai8ktcHyAWo4I4zu6dAd9Fbz8aehEbAcJo'

    if acme_data != expected_request:
        return HttpResponseNotFound()

    return HttpResponse(
        'lX8D7FNGoai8ktcHyAWo4I4zu6dAd9Fbz8aehEbAcJo.'
        'fL5DxaUDxd_IosDayHDs9HS4kGtc2XVCiQbOdyAg340'
    )
