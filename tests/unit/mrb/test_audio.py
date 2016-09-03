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

from unittest import TestCase
from unittest.mock import (
    mock_open,
    patch,
    MagicMock,
)

from discord import VoiceClient
from discord.voice_client import StreamPlayer

from mrb import run_audio_file


class TestAudioFunctions(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected_file_path = "/foo/bar/file.ext"
        cls.mock_open_reference = "mrb.audio.open"

    def setUp(self):
        self.mocked_open = mock_open()

        self.player = MagicMock(spec=StreamPlayer)
        self.player.is_playing = MagicMock(return_value=False)

        self.voice_client = MagicMock(spec=VoiceClient)
        self.voice_client.create_ffmpeg_player = MagicMock(return_value=self.player)

    def test_file_opened(self):
        expected_calls = [
            [self.expected_file_path, 'rb'],
            ['/dev/null', 'w'],
        ]

        with patch(self.mock_open_reference, self.mocked_open):
            run_audio_file(self.expected_file_path, self.voice_client)

        for expected_call in expected_calls:
            self.mocked_open.assert_any_call(*expected_call)

    def test_ffmpeg_opened(self):
        file_open_objects = [
            mock_open().return_value,
            mock_open().return_value,
        ]

        self.mocked_open.side_effect = file_open_objects

        with patch(self.mock_open_reference, self.mocked_open):
            run_audio_file(self.expected_file_path, self.voice_client)

        self.voice_client.create_ffmpeg_player.assert_called_with(
            file_open_objects[0],
            pipe=True,
            stderr=file_open_objects[1],
        )

    def test_ffmpeg_volume_custom(self):
        expected_volume = 0.5

        with patch(self.mock_open_reference, self.mocked_open):
            run_audio_file(self.expected_file_path, self.voice_client, expected_volume)

        self.assertEqual(self.player.volume, expected_volume)

    def test_ffmpeg_volume_default(self):
        with patch(self.mock_open_reference, self.mocked_open):
            run_audio_file(self.expected_file_path, self.voice_client)

        self.assertEqual(self.player.volume, 1.0)
