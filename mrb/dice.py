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

from random import randint
from typing import List


def _poor_mans_try_parse(input_string: str) -> bool:
    """
    Give any string, determine if the string can be converted to an `int`.

    :param input_string: The input string to parse
    :return: `True` if int(input_string) succeeds, `False` otherwise.
    """

    try:
        _ = int(input_string)
        return True
    except ValueError:
        return False


def roll_dice(count: int, sides: int) -> List[int]:
    """
    Roll a give type of die or dice.

    :param count: The number of dice to roll
    :param sides: The number of sides per die
    :return: A list of integers representing the rolled dice
    """

    result = []

    for die in range(count):
        result.append(randint(1, sides))

    return result


def roll(input_string: str='') -> List[int]:
    """
    Given an arbitrary input string, parse out and perform a "roll" of dice.

    For example, inputting "2d20" would roll TWO dice with TWENTY sides
    each.

    :raises: `ValueError` on parse failure. Will contain a readable message.

    :param input_string: The string to parse
    :return: A list of integers representing the rolled dice
    """

    delimiter = 'd'
    dice_limit = 10
    side_limit = 20
    invalid_format_msg = "Expected format `NdM`! For example, `2d20`"

    # Verify there is only one delimiter on input
    if input_string.count(delimiter) != 1:
        raise ValueError(invalid_format_msg)

    # Split to get [number of dice, sides per dice]
    input_split = input_string.split(delimiter)
    if len(input_split) != 2:
        raise ValueError(invalid_format_msg)

    # If any of these fail to parse out, bail out
    if not all(_poor_mans_try_parse(x) for x in input_split):
        raise ValueError(invalid_format_msg)

    # Parse values to ints
    number_of_dice = int(input_split[0])
    sides_per_die = int(input_split[1])

    # Verify everything is above zero
    if any(x <= 0 for x in [number_of_dice, sides_per_die]):
        raise ValueError("You can't input non-positive numbers!")

    # Raise exception on too many dice
    if number_of_dice > dice_limit:
        raise ValueError(
            "You can't roll more than {} dice at once!".format(dice_limit)
        )

    # Raise exception on too many sides
    if sides_per_die > side_limit:
        raise ValueError(
            "You can't roll a die with more than {} sides!".format(side_limit)
        )

    # So we have valid input, within logical bounds. Roll em!
    return roll_dice(count=number_of_dice, sides=sides_per_die)
