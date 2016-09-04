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

import hashlib
import os

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
        # noinspection SpellCheckingInspection
        self.hash_checks = {
            'collar':
                'b71e8ab0c3920370847543ef0e80a588f06b399dcd2857ee2fb1ee4e2ddb32f6',
            'djkhaled':
                '42b195ef28ecebcceed88faac89f805ad1369d7e19db55268e57adaf018a85d0',
            'runorcurse':
                'e3d98cdeca8c414e1361893d530514640e82f9cdfc735069b6f0557c4ad1dac8',
        }

        self.sound_files = {}

        path = "{}/sounds/".format(
            os.path.dirname(os.path.abspath(__file__))
        )

        for entry in os.scandir(path):
            if not entry.is_file() or entry.name not in self.hash_checks:
                continue

            with open(entry.path, "rb") as sound_file:
                data = sound_file.read()
                if hashlib.sha256(data).hexdigest() != self.hash_checks[entry.name]:
                    continue

                self.sound_files[entry.name] = data


if __name__ == '__main__':
    x = Player()
    _ = 1
