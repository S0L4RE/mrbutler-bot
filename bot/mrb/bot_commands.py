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

import logging
from typing import (
    Callable,
    Dict,
    Optional,
    Tuple,
)

from discord import Message

from mrb_common.commanding import (
    Commander,
    CommandResult,
)
from .versioning import get_version_command


class BotCommands(Commander):
    """Customize, and define, the commands for our main commander in the bot"""

    def __init__(self, logger: logging.Logger):
        super().__init__()

        self._logger = logger

        self.configure_commands({
            '!version': (
                get_version_command,
                "I'll report my current version number to you",
            ),
        })

    def configure_commands(
            self,
            raw_commands: Dict[str, Tuple[Callable, str]],
    ):
        """Configure the commands for this bot, from a raw structure"""
        for trigger, raw_command in raw_commands.items():
            command, help_text = raw_command
            self.add(
                trigger=trigger,
                command=command,
                help_text=help_text,
            )

    def execute(
            self,
            trigger: str,
            message: Message,
    ):
        """Prevent direct access to execute from this class"""
        raise NotImplementedError("'execute' is not allowed here!")

    def parse_message(self, message: Message) -> Optional[CommandResult]:
        """Parse a given message for a command token and execute"""
        tokens = message.content.split()
        self._logger.log(logging.DEBUG, "tokens: {}".format(tokens))

        command_token = tokens[0] if len(tokens) > 0 else ''
        self._logger.log(
            logging.DEBUG,
            "command_token: {}".format(command_token)
        )

        return super().execute(command_token, message)
