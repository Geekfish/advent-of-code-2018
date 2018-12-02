import pytest


def calculate_frequency(operations):
    return sum(map(int, operations))


def test_calculate_frequency_single_addition():
    assert calculate_frequency(["+10"]) == 10


def test_calculate_frequency_single_subtraction():
    assert calculate_frequency(["-10"]) == -10


@pytest.mark.parametrize(
    "operations,result",
    (
        (("+10", "-2"), 8),
        (("+10", "-2", "-10", "-8", "+1", "+1000"), 991),
        (("0", ), 0),
        (("0", "+1", "-1", "+0"), 0),
    )
)
def test_calculate_frequency_many_lines(operations, result):
    assert calculate_frequency(operations) == result


def main():
    with open("input.txt", "r") as f:
        operations = f.readlines()
    print(calculate_frequency(operations))


if __name__ == '__main__':
    main()
