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

import os
from asyncio import sleep
from collections import OrderedDict
from typing import List

from discord import VoiceClient


def run_audio_file(
        file_path: str,
        voice_channel:
        VoiceClient, volume: float=1.0
):
    """
    Play a given audio file over a given voice client.

    :param file_path: Path to the audio file on disk.
    :param voice_channel: The `VoiceClient` to play the audio over.
    :param volume: (Optional) the volume to play the audio at.
    """

    with open(file_path, "rb") as audio_file:
        player = voice_channel.create_ffmpeg_player(
            audio_file,
            pipe=True,
            stderr=open('/dev/null', 'w'),
        )

        player.volume = volume
        player.start()

        while player.is_playing():
            pass


class Player(object):
    def __init__(self):
        self._sound_files = {}

        path = "{}/sounds/".format(
            os.path.dirname(os.path.abspath(__file__))
        )

        for entry in os.scandir(path):
            if not entry.is_file():
                continue

            self._sound_files[entry.name] = entry.path

    @property
    def sound_names(self) -> List[str]:
        return sorted(list(self._sound_files.keys()))

    @property
    def sound_files(self) -> OrderedDict:
        return OrderedDict(sorted(self._sound_files.items()))

    async def play(
        self,
        audio_name_to_play: str,
        voice_client: VoiceClient,
    ):
        """
        Play a given audio file over a given voice client.

        :param audio_name_to_play: Path to the audio file on disk.
        :param voice_client: The `VoiceClient` to play the audio over.
        """

        if audio_name_to_play not in self._sound_files:
            return

        player = voice_client.create_ffmpeg_player(
            filename=self._sound_files[audio_name_to_play],
            stderr=open('/dev/null', 'w'),
        )
        player.start()

        while player.is_playing():
            await sleep(0.5)
