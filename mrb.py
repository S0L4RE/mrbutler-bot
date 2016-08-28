#! /usr/bin/env python

import logging
import random
import sys

import discord

import mrb
from mrb import MrbEnvironment

stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(logging.Formatter('%(asctime)s %(levelname)s - %(message)s'))
stdout_logger.setLevel(logging.DEBUG)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
logger.addHandler(stdout_logger)

# Get the env details
bot_env = MrbEnvironment()

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

    # This prevents anyone except for the bot's admin from running commands
    if message.author.id != bot_env.DiscordAdminId:
        return

    if message.content.startswith('!help'):
        commands = (
            "I understand the following commands:\n\n"
            "```\n"
            "!d20 -------- I'll roll a D20 die.\n"
            "!djkhaled --- I'll remind you that you're smart\n"
            "!help ------- I'll send you this command list.\n"
            "!hello ------ I'll say hello to you!\n"
            "```\n"
            "Mr. Butler, version `{0}`, at your service."
        ).format(mrb.__version__)

        await client.send_message(message.author, commands)
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
        return

    if message.content.startswith('!d20'):
        roll = random.randrange(1, 21)
        msg = '{0} rolled a {1}'.format(
            message.author.mention,
            roll,
        )
        await client.send_message(message.channel, msg)
        return

    if message.content.startswith('!djkhaled'):
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
