#! /usr/bin/env python

import logging
import random
import os
import sys

import datetime
import discord

stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(logging.Formatter('%(asctime)s %(levelname)s - %(message)s'))
stdout_logger.setLevel(logging.DEBUG)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(stdout_logger)

discord_token_key = "MRB_DISCORD_TOKEN"
discord_token = os.getenv('MRB_DISCORD_TOKEN', None)
if discord_token is None:
    print("Could not load discord token!")
    print("Did you set '{}' ?".format(discord_token_key))
    exit(-1)

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        commands = (
            "I understand the following commands:\n\n"
            "```\n"
            "!d20 ----- I'll roll a D20 die.\n"
            "!help ---- I'll send you this command list.\n"
            "!hello --- I'll say hello to you!\n"
            "```\n"
            "Mr. Butler, at your service."
        )

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
        player = voice.create_ffmpeg_player('./static/djkhaled.wav')
        player.volume = 0.3
        player.start()

        while player.is_playing():
            pass

        await voice.disconnect()
        return


@client.event
async def on_ready():
    logger.log(logging.INFO, '---')
    logger.log(logging.INFO, 'Logged in as')
    logger.log(logging.INFO, client.user.name)
    logger.log(logging.INFO, client.user.id)
    logger.log(logging.INFO, '---')


if __name__ == '__main__':
    client.run(discord_token)
