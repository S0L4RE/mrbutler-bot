#! /usr/bin/env python

import hashlib
import logging
import os
import random
import sys
import tempfile
import urllib.request

import discord

stdout_logger = logging.StreamHandler(sys.stdout)
stdout_logger.setFormatter(logging.Formatter('%(asctime)s %(levelname)s - %(message)s'))
stdout_logger.setLevel(logging.DEBUG)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(stdout_logger)

discord_token_key = "MRB_DISCORD_TOKEN"
discord_token = os.getenv(discord_token_key, None)
if discord_token is None:
    print("Could not load discord token!")
    print("Did you set '{}' ?".format(discord_token_key))
    exit(-1)

discord_admin_key = "MRB_ADMIN_ID"
discord_admin = os.getenv(discord_admin_key, None)
if discord_admin is None:
    print("Could not load discord token!")
    print("Did you set '{}' ?".format(discord_token_key))
    exit(-2)

client = discord.Client()
audio_data = {}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.id != discord_admin:
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
        data_file = audio_data.get("djkhaled", None)
        if data_file is None:
            return

        temp = tempfile.TemporaryFile(mode="w+b")
        temp.write(data_file)
        temp.seek(0)

        voice = await client.join_voice_channel(message.author.voice_channel)

        try:
            voice.encoder_options(sample_rate=48000, channels=2)
            player = voice.create_ffmpeg_player(temp, pipe=True, stderr=open('/dev/null', 'w'))
            player.volume = 0.3
            player.start()

            while player.is_playing():
                pass
        except discord.DiscordException:
            await client.send_message(message.channel, "Something went wrong `:(`")
        finally:
            await voice.disconnect()

        return

    if message.content.startswith('!purge'):
        if message.author.id != discord_admin:
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
    logger.log(logging.INFO, "Downloading audio...")

    url = "https://urda.github.io/discord-mr-butler/static/djkhaled.wav"
    url_sha256 = "42b195ef28ecebcceed88faac89f805ad1369d7e19db55268e57adaf018a85d0"
    response = urllib.request.urlopen(url)
    data = response.read()
    if hashlib.sha256(data).hexdigest() == url_sha256:
        audio_data['djkhaled'] = data
        logger.log(logging.INFO, "Downloaded DJ KHALED")
    else:
        logger.log(logging.WARNING, "Failed to download DJ KHALED")


if __name__ == '__main__':
    client.run(discord_token)
