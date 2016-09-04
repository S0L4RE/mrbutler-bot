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
