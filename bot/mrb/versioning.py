"""
Copyright 2017 Peter Urda

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

from discord import Message

from mrb_common.commanding import (
    CommandResult,
    ResponseType,
)


def get_version() -> str:
    """Get the raw version string"""
    return '0.3.3'


def get_version_command(message: Message) -> CommandResult:
    """Generate a version response"""
    response = (
        '{user} I am version `{version}` and at your service.'
    ).format(
        user=message.author.mention,
        version=get_version(),
    )

    return CommandResult(
        content=response,
        response_type=ResponseType.ChannelMessage,
        success=True,
    )
