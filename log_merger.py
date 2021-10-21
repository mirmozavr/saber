import json
import os
from datetime import datetime as dt

import click


def check_input(path1: str, path2: str, o: str) -> None:
    for path in path1, path2:
        if not os.path.isfile(path):
            print(f"'{path}' is not a file. Choose a new one.")
            quit()
    if os.path.isfile(o):
        print(f"'{o}' already exists. Choose a new one.")
        quit()
    os.makedirs(os.path.dirname(o), exist_ok=True)
    print("Folders checked. All OK")


def merge(path1: str, path2: str, o: str) -> None:
    start_time = dt.now()
    print(f"Merge started at {start_time.strftime('%H:%M:%S')}")
    with open(path1) as log_a, open(path2) as log_b, open(o, "w") as file:
        a, b = log_a.readline(), log_b.readline()
        if a and b:
            while True:
                if not (a and b):
                    file.write(json.dumps(a) if a else json.dumps(b))
                    file.write("\n")
                    break

                if isinstance(a, str):
                    a = json.loads(a)
                if isinstance(b, str):
                    b = json.loads(b)

                if a["timestamp"] <= b["timestamp"]:
                    file.write(json.dumps(a))
                    a = log_a.readline()
                else:
                    file.write(json.dumps(b))
                    b = log_b.readline()
                file.write("\n")
        else:
            file.write(a or b)

        [file.write(line) for line in log_a.readlines()]
        [file.write(line) for line in log_b.readlines()]

    end_time = dt.now()
    print(
        f"Merge ended at {end_time.strftime('%H:%M:%S')}\n"
        f"Elapsed time: {(end_time-start_time).seconds} second"
    )


@click.command()
@click.argument("path1", required=True)
@click.argument("path2", required=True)
@click.option("-o", required=True, help="Path to merged log file")
def main(path1: str, path2: str, o: str):
    """PATH1 and PATH2 are log files to be merged"""
    check_input(path1, path2, o)
    merge(path1, path2, o)


if __name__ == "__main__":
    main()
