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

from typing import Callable

from discord import Message

from .command_result import CommandResult


class Command(object):
    def __init__(
            self,
            command: Callable[[Message], CommandResult],
            help_text: str=''
    ):
        """
        Class to represent a "command" for the bot to respond and act on.

        :param command: The actual function to fire
        :param help_text: The help text for more information
        """

        self.command = command
        self.help_text = help_text

    def execute(self, message: Message) -> CommandResult:
        """
        Execute the function stored in this command

        :param message: The discord message to pass to the function
        :return: The CommandResult from the function
        """
        return self.command(message)
