#! /usr/bin/env python

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

import logging
import sys

import discord

import mrb

stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(logging.Formatter('%(asctime)s %(levelname)s - %(message)s'))
stdout_logger.setLevel(logging.DEBUG)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger.addHandler(stdout_logger)

# Get the env details
bot_env = mrb.MrbEnvironment()

for check_env_key, check_env_value in bot_env.environment.items():
    if check_env_value is None:
        print("Could not load required environment variable!")
        print("Did you set '{}' ?".format(check_env_key))
        exit(-1)

client = discord.Client()
audio_data = {}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        commands = (
            "I understand the following commands:\n\n"
            "```\n"
            "!djkhaled --- I'll remind you that you're smart\n"
            "!help ------- I'll send you this command list.\n"
            "!hello ------ I'll say hello to you!\n"
            "!roll NdM --- I'll roll 'N' number of dice with 'M' sides\n"
            "```\n"
            "Mr. Butler, version `{0}`, at your service."
        ).format(mrb.__version__)

        await client.send_message(message.author, commands)
        return

    if message.content.startswith('!roll'):
        # If a message is longer than 15 characters, don't trust it!
        # len('!roll 10d20') = 11, 15 is more than enough.
        safe_length = 15
        invalid_format_msg = "Expected format `NdM`! For example, `2d20`"
        invalid_too_long = "That message was too long and will not be parsed. {}".format(invalid_format_msg)
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
            return

        try:
            roll_result = mrb.roll(roll_string_input[1])

            msg = "{0} rolled".format(message.author.mention)

            if roll_result > 1:
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
            return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        return

    if message.content.startswith('!djkhaled'):
        if message.author.id != bot_env.DiscordAdminId:
            msg = "You are not in the sudo'ers file {}".format(message.author.mention)
            await client.send_message(message.author, msg)
            return

        voice = await client.join_voice_channel(message.author.voice_channel)

        try:
            with open("/mrb/media/djkhaled.wav", "rb") as f:
                voice.encoder_options(sample_rate=48000, channels=2)
                player = voice.create_ffmpeg_player(f, pipe=True, stderr=open('/dev/null', 'w'))
                player.volume = 0.2
                player.start()

                while player.is_playing():
                    pass
        except discord.DiscordException:
            await client.send_message(message.channel, "Something went wrong `:(`")
        finally:
            await voice.disconnect()

        return

    if message.content.startswith('!purge'):
        if message.author.id != bot_env.DiscordAdminId:
            msg = "You are not in the sudo'ers file {}".format(message.author.mention)
            await client.send_message(message.author, msg)
            return

        await client.purge_from(message.channel)
        await client.send_message(message.channel, "Purged")


@client.event
async def on_ready():
    logger.log(logging.INFO, '---')
    logger.log(logging.INFO, 'Logged in as')
    logger.log(logging.INFO, client.user.name)
    logger.log(logging.INFO, client.user.id)
    logger.log(logging.INFO, '---')
    logger.log(logging.INFO, 'ENV VARS:')

    for env_key, env_value in bot_env.environment.items():
        logger.log(logging.INFO, '{0:.<25} {1}'.format(env_key + " ", env_value))

    logger.log(logging.INFO, '---')
    logger.log(logging.INFO, "Version: '{}'".format(mrb.__version__))
    logger.log(logging.INFO, '---')


if __name__ == '__main__':
    client.run(bot_env.DiscordToken)
