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


def run_audio_file(file_path: str, voice_channel: VoiceClient, volume: float):
    with open(file_path, "rb") as f:
        player = voice_channel.create_ffmpeg_player(f, pipe=True, stderr=open('/dev/null', 'w'))
        player.volume = volume
        player.start()

        while player.is_playing():
            pass
