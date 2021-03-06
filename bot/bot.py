#! /usr/bin/env python

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

import asyncio
import logging
import sys
from typing import List

import discord

import mrb
import mrb.environment
import mrb.fun
import mrb.versioning
from mrb_common.commanding import ResponseType

# Get the env details
bot_env = mrb.environment.Environment()

for check_env_key, check_env_value in bot_env.env_vars_ordered.items():
    if check_env_value is None:
        print("Could not load required environment variable!")
        print("Did you set '{}' ?".format(check_env_key))
        exit(-1)

if bot_env.type == mrb.environment.EnvironmentType.DEV:
    log_level = logging.DEBUG
else:
    log_level = logging.INFO

stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(
    logging.Formatter(
        '{asctime} - {levelname: <8} - {module} - {message}',
        style='{',
    )
)
stdout_logger.setLevel(log_level)

logger = logging.getLogger('discord')
logger.setLevel(log_level)
logger.addHandler(stdout_logger)

client = discord.Client()
player = mrb.Player()

bot_raw_commands = {
    '!version': (
        mrb.versioning.get_version_command,
        "I'll report my current version number to you",
    ),
}

bot_commands = mrb.BotCommands(
    commands=bot_raw_commands,
    logger=logger,
)


def get_help_message(audio_list: List[str]=None) -> str:
    help_message = (
        "I understand the following commands:\n"
        "```\n"
        "{0}\n"
        "```\n"
        "\n"
        "{1}"
        "**I do not respond to DM's.**\n"
    )

    commands = [
        ("!help", "I'll send you this command list"),
        ("!hello", "I'll say hello to you"),
        ("!play sound-name", "I'll play a sound for you (see list below)"),
        ("!roll NdM", "I'll roll 'N' number of dice with 'M' sides"),
        ("!version", "I'll report my current version number to you"),
    ]
    command_message_list = []
    for (command_name, command_help_text) in commands:
        command_message_list.append(
            "{0:.<20} {1}".format(command_name + " ", command_help_text),
        )

    if audio_list:
        audio_player_help_message = (
            "I can `!play` the following:\n"
            "```\n"
            "{0}\n"
            "```\n"
            "\n"
        ).format("\n".join(audio_list))
    else:
        audio_player_help_message = '`!play` is unavailable at this time.\n\n'

    return help_message.format(
        "\n".join(command_message_list),
        audio_player_help_message,
    )


@client.event
async def on_message(message):
    # Ignore the bot's own messages
    if message.author == client.user:
        return

    # Ignore private messages
    if message.channel.type == discord.ChannelType.private:
        return

    # Run commander
    command_result = bot_commands.parse_message(message)
    if command_result and command_result.success:
        send_message_types = {
            ResponseType.ChannelMessage: message.channel,
            ResponseType.DirectMessage: message.author,
        }

        if command_result.response_type in send_message_types:
            await client.send_message(
                destination=send_message_types[command_result.response_type],
                content=command_result.content,
            )

        return

    if message.content.startswith('!help'):
        await client.send_message(
            message.author,
            get_help_message(player.sound_names),
        )
        await client.delete_message(message)
        return

    if message.content.startswith('!roll'):
        # If a message is longer than 15 characters, don't trust it!
        # len('!roll 10d20') = 11, 15 is more than enough.
        safe_length = 15
        invalid_format_msg = "Expected format `NdM`! For example, `2d20`"
        invalid_too_long = \
            "That message was too long and will not be parsed. {}".format(
                invalid_format_msg
            )
        invalid_pm_template = "I didn't understand that {0}. {1}"
        log_message_template = "Caught exception from user {0} --- {1}"

        if len(message.content) > safe_length:
            msg = invalid_pm_template.format(
                message.author.mention,
                invalid_too_long,
            )
            logger.log(
                logging.WARNING,
                log_message_template.format(
                    message.author,
                    msg,
                ),
            )
            await client.send_message(message.author, msg)
            await client.delete_message(message)
            return

        roll_string_input = message.content.split(' ')

        # If we couldn't get input to try and roll, return
        if len(roll_string_input) < 2:
            msg = invalid_pm_template.format(
                message.author.mention,
                invalid_format_msg,
            )
            logger.log(
                logging.WARNING,
                log_message_template.format(
                    message.author,
                    msg,
                ),
            )
            await client.send_message(message.author, msg)
            await client.delete_message(message)
            return

        try:
            roll_result = mrb.fun.Dice.roll(roll_string_input[1])

            msg = "Given a `{0}` {1} rolled".format(
                roll_string_input[1],
                message.author.mention,
            )

            if len(roll_result) > 1:
                msg = "{0} `{1}` for a total of `{2}`".format(
                    msg,
                    roll_result,
                    sum(roll_result),
                )
            else:
                msg = "{0} a `{1}`".format(
                    msg,
                    roll_result[0],
                )

            await client.send_message(message.channel, msg)
            await client.delete_message(message)
            return

        except ValueError as e:
            msg = invalid_pm_template.format(message.author.mention, e)
            logger.log(
                logging.WARNING,
                log_message_template.format(
                    message.author,
                    msg,
                ),
            )
            await client.send_message(message.author, msg)
            await client.delete_message(message)
            return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        return

    if message.content.startswith('!play'):
        requested = message.content[len('!play'):].strip()

        await client.delete_message(message)

        if requested not in player.sound_names:
            msg = "I could not find `{0}` in my sound list {1}".format(
                requested,
                message.author.mention,
            )
            logger.log(
                logging.WARNING,
                "Caught exception from user {0} - {1} --- {2}".format(
                    message.author,
                    message.author.id,
                    msg,
                ),
            )
            await client.send_message(message.author, msg)
            return

        logger.log(logging.INFO, "{0} - {1} ran audio '{2}'".format(
            message.author,
            message.author.id,
            requested,
        ))

        if message.author.voice_channel is None:
            msg = "You need to be connected to a voice channel!".format(
                requested,
                message.author.mention,
            )
            logger.log(
                logging.WARNING,
                "Caught exception from user {0} - {1} --- {2}".format(
                    message.author,
                    message.author.id,
                    msg,
                ),
            )
            await client.send_message(message.author, msg)
            return

        try:
            voice = await client.join_voice_channel(
                message.author.voice_channel
            )
        except asyncio.TimeoutError:
            logger.log(
                logging.ERROR,
                (
                    "Audio connection timed out for '{0}' "
                    "on server '{1} --- {2}' on channel '{3}'. "
                    "Called by user '{4} --- {5}'"
                ).format(
                    requested,
                    message.server.id,
                    message.server.name,
                    message.author.voice_channel,
                    message.author.id,
                    message.author,
                )
            )
            msg = (
                "I was unable to connect to your voice channel `{0}` "
                "on discord server `{1}`. "
                "I may not have permission to connect to it!"
            ).format(
                message.author.voice_channel,
                message.server.name,
            )
            await client.send_message(message.author, msg)
            return

        try:
            await player.play(requested, voice)
        except discord.DiscordException:
            logger.log(logging.ERROR, "Failed to run '{}'".format(requested))
        finally:
            await voice.disconnect()

        return


@client.event
async def on_ready():
    logger.log(logging.INFO, '---')
    logger.log(logging.INFO, 'Logged in as:')
    logger.log(logging.INFO, "{name} - {id}".format(
        name=client.user.name,
        id=client.user.id,
    ))

    logger.log(logging.INFO, '---')
    logger.log(logging.INFO, 'ENV VARS:')
    for env_key, env_value in bot_env.env_vars_ordered.items():
        logger.log(
            logging.INFO,
            '{0:.<25} {1}'.format(env_key + " ", env_value)
        )

    logger.log(logging.INFO, '---')
    logger.log(logging.INFO, 'SOUNDS LOADED:')
    for sound_name, sound_file in player.sound_files.items():
        logger.log(
            logging.INFO,
            "{0:.<17} {1}".format(sound_name + " ", sound_file)
        )

    logger.log(logging.INFO, '---')
    logger.log(
        logging.INFO,
        "Version: '{}'".format(mrb.versioning.get_version()),
    )

    logger.log(logging.INFO, '---')


if __name__ == '__main__':
    client.run(bot_env.discord_token)
