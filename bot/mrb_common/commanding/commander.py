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

from typing import (
    Callable,
    Optional,
)

from discord import Message

from .command import Command
from .command_result import CommandResult


class Commander(object):
    def __init__(self):
        # Define object attributes to avoid
        # "Instance attribute defined outside __init__"
        self._commands = None
        self._help_text_block = None

        # Actually configure the Commander
        self.reset()

    @property
    def help_text(self) -> str:
        """
        Generate a formatted string to display triggers and help text together

        :return: The commands, in a single string, as a help text block
        """
        # If the help text block is already set, just return it
        if self._help_text_block:
            return self._help_text_block

        # Else, we need to go ahead and compute it from the current commands
        help_text_block_lines = []
        for trigger, command in sorted(self._commands.items()):
            help_text_block_lines.append(
                "{trigger:.<30} {help_text}".format(
                    trigger=trigger + " ",
                    help_text=command.help_text,
                )
            )

        self._help_text_block = "\n".join(help_text_block_lines)
        return self._help_text_block

    def add(
            self,
            trigger: str,
            command: Callable[[Message], CommandResult],
            help_text: str=''
    ):
        """
        Add a command to the commander.

        Raises a KeyError if a command already exists with a given trigger.

        :param trigger: The keyword for this command
        :param command: The function for this command
        :param help_text: The help text, if available, for more information
        """

        if trigger in self._commands:
            raise KeyError("Command '{}' already exists!".format(trigger))

        self._commands[trigger] = Command(command, help_text)

        # Invalidate help text block
        self._help_text_block = None

    def execute(
            self,
            trigger: str,
            message: Message,
    ) -> Optional[CommandResult]:
        """
        Have the commander run a desired command from a given trigger.

        :param trigger: The trigger to execute
        :param message: The discord message to act on
        :return: A `CommandResult` object, or `None` if no command ran
        """

        # If there's no matching command listing, just stop now
        if trigger not in self._commands:
            return None

        return self._commands[trigger].execute(message)

    def remove(self, trigger: str):
        """
        Remove a command from the commander.

        Raises a KeyError if a command does not exist with a given trigger.

        :param trigger: The keyword of the command to remove
        """

        if trigger not in self._commands:
            raise KeyError("Command '{}' not found!".format(trigger))

        del self._commands[trigger]

        # Invalidate help text block
        self._help_text_block = None

    def reset(self):
        """Reset the commander to the initial state"""
        self._commands = {}
        self._help_text_block = None
