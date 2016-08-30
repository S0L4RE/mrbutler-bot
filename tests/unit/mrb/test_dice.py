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


class TestRoll(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected_dice_limit = 10
        cls.expected_side_limit = 20

        cls.expected_base_message = "Expected format `NdM`! For example, `2d20`"
        cls.expected_dice_limit_message = \
            "You can't roll more than {} dice at once!".format(
                cls.expected_dice_limit
            )
        cls.expected_non_positive_message = \
            "You can't input non-positive numbers!"
        cls.expected_side_limit_message = \
            "You can't roll a die with more than {} sides!".format(
                cls.expected_side_limit
            )

    def test_dice_limit(self):
        with self.assertRaises(ValueError) as roll_exception:
            roll(
                "{0}d{1}".format(
                    self.expected_dice_limit + 1,
                    self.expected_side_limit,
                )
            )

        self.assertEqual(
            str(roll_exception.exception),
            self.expected_dice_limit_message,
        )

    def test_missing_delimiter(self):
        with self.assertRaises(ValueError) as roll_exception:
            roll("missing_info")

        self.assertEqual(
            str(roll_exception.exception),
            self.expected_base_message,
        )

    def test_negative_ints(self):
        with self.assertRaises(ValueError) as roll_exception_left:
            roll("-1d20")

        with self.assertRaises(ValueError) as roll_exception_right:
            roll("1d-20")

        self.assertEqual(
            str(roll_exception_left.exception),
            self.expected_non_positive_message,
        )

        self.assertEqual(
            str(roll_exception_right.exception),
            self.expected_non_positive_message,
        )

    def test_parse_int_fail(self):
        with self.assertRaises(ValueError) as roll_exception:
            roll("NotANumber_d20")

        self.assertEqual(
            str(roll_exception.exception),
            self.expected_base_message,
        )

    def test_side_limit(self):
        with self.assertRaises(ValueError) as roll_exception:
            roll(
                "{0}d{1}".format(
                    self.expected_dice_limit,
                    self.expected_side_limit + 1,
                )
            )

        self.assertEqual(
            str(roll_exception.exception),
            self.expected_side_limit_message,
        )

    def test_zero_values(self):
        with self.assertRaises(ValueError) as roll_exception_zero_left:
            roll("0d20")

        with self.assertRaises(ValueError) as roll_exception_zero_right:
            roll("10d0")

        with self.assertRaises(ValueError) as roll_exception_zero_left_pad:
            roll("000d20")

        with self.assertRaises(ValueError) as roll_exception_zero_right_pad:
            roll("10d000")

        check_list = [
            roll_exception_zero_left,
            roll_exception_zero_left_pad,
            roll_exception_zero_right,
            roll_exception_zero_right_pad,
        ]

        for exception in check_list:
            self.assertEqual(
                str(exception.exception),
                self.expected_non_positive_message,
            )
