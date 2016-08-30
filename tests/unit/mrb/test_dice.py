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

from mrb import roll
from mrb.dice import (
    poor_mans_try_parse,
    roll_dice,
)


class TestDice(TestCase):
    def test_poor_mans_try_parse(self):
        self.assertTrue(poor_mans_try_parse("-1"))
        self.assertTrue(poor_mans_try_parse("0"))
        self.assertTrue(poor_mans_try_parse("1"))
        self.assertTrue(poor_mans_try_parse("01"))

        self.assertFalse(poor_mans_try_parse("invalid"))
        self.assertFalse(poor_mans_try_parse("one"))

    def test_roll_dice(self):
        test_data = [
            (1, 6),
            (5, 10),
            (10, 20),
            (20, 100),
        ]

        for dice_to_roll, dice_side_count in test_data:
            rolls = roll_dice(dice_to_roll, dice_side_count)
            self.assertEqual(len(rolls), dice_to_roll)

            for roll_result in rolls:
                self.assertGreaterEqual(roll_result, 1)
                self.assertLessEqual(roll_result, dice_side_count)
