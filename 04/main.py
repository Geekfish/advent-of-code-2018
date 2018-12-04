from typing import Sequence


def choose_guard(observation_entries: Sequence[str]) -> int:
    pass


def main():
    with open("input.txt", "r") as f:
        observation_entries = f.readlines()
    print(choose_guard(observation_entries))


if __name__ == "__main__":
    main()
