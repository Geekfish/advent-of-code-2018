from itertools import cycle

import pytest


def find_double_frequency(operations):
    operations = cycle(operations)
    past_frequencies = [0]
    for operation in operations:
        frequency = past_frequencies[-1] + int(operation)
        if frequency in past_frequencies:
            return frequency
        past_frequencies.append(frequency)


def test_find_double_frequency_just_two():
    assert find_double_frequency(["+1", "-1"]) == 0


@pytest.mark.parametrize(
    "operations,result",
    (
        (("+3", "+3", "+4", "-2", "-4"), 10),
        (("-6", "+3", "+8", "+5", "-6"), 5),
        (("+7", "+7", "-2", "-7", "-4"), 14),
    ),
)
def test_find_double_frequency_many(operations, result):
    assert find_double_frequency(operations) == result


def main():
    with open("input.txt", "r") as f:
        operations = f.readlines()
    print(find_double_frequency(operations))


if __name__ == "__main__":
    main()
