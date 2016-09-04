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

from mrb import Player


class TestPlayer(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_open_reference = "mrb.audio.player.open"

    def setUp(self):
        self.mocked_open = mock_open()

        self.ffmpeg_player = MagicMock(spec=StreamPlayer)
        self.ffmpeg_player.is_playing = MagicMock(return_value=False)

        self.voice_client = MagicMock(spec=VoiceClient)  # type: VoiceClient
        self.voice_client.create_ffmpeg_player = MagicMock(
            return_value=self.ffmpeg_player
        )

        self.player = Player()
        self.sample_file = self.player.sound_names[0]
        self.sample_file_path = self.player.sound_files[self.sample_file]

    def test_ffmpeg_player_create(self):
        dev_null_reference = mock_open().return_value

        self.mocked_open.return_value = dev_null_reference

        with patch(self.mock_open_reference, self.mocked_open):
            self.player.play(self.sample_file, self.voice_client)

        # noinspection PyUnresolvedReferences
        self.voice_client.create_ffmpeg_player.assert_called_with(
            filename=self.sample_file_path,
            stderr=dev_null_reference,
        )

    def test_ffmpeg_player_dev_null_opened(self):
        with patch(self.mock_open_reference, self.mocked_open):
            self.player.play(self.sample_file, self.voice_client)

        self.mocked_open.assert_called_once_with('/dev/null', 'w')

    def test_ffmpeg_player_starts(self):
        with patch(self.mock_open_reference, self.mocked_open):
            self.player.play(self.sample_file, self.voice_client)

        self.assertEqual(self.ffmpeg_player.start.call_count, 1)

    def test_ffmpeg_player_waits_to_finish(self):
        side_effects = [True, False]

        self.ffmpeg_player.is_playing = MagicMock(side_effect=side_effects)
        self.voice_client.create_ffmpeg_player = MagicMock(
            return_value=self.ffmpeg_player,
        )

        with patch(self.mock_open_reference, self.mocked_open):
            self.player.play(self.sample_file, self.voice_client)

        self.assertEqual(
            self.ffmpeg_player.is_playing.call_count,
            len(side_effects),
        )

    def test_invalid_name_request(self):
        with patch(self.mock_open_reference, self.mocked_open):
            self.player.play("No such file", self.voice_client)

        self.ffmpeg_player.start.assert_not_called()
        self.ffmpeg_player.is_playing.assert_not_called()
        # noinspection PyUnresolvedReferences
        self.voice_client.create_ffmpeg_player.assert_not_called()
