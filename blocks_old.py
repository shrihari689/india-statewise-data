import requests
import csv
import json
import os

BLOCK_FILE = "https://raw.githubusercontent.com/planemad/india-local-government-directory/master/statistical/blocks.csv"


def parameterize(word: str) -> str:
    return word.replace(" ", "_").lower().strip()


def create_directories(path):
    if not os.path.exists(path):
        os.makedirs(path)


def dump_file(data, type):
    state = parameterize(data["state"])
    district = parameterize(data["district"])
    block = parameterize(data["block"])
    block_code = parameterize(data["block_code"])
    path = f"data/{state}/{district}/{type}"

    create_directories(path)

    with open(f"{path}/{block_code}.json", "w") as file:
        file.write(json.dumps(data))
    pass


if __name__ == "__main__":
    file = requests.get(BLOCK_FILE).text
    csv_file = csv.reader(file.splitlines()[1:], delimiter=",")
    for i in csv_file:
        state = i[2]
        district = i[4]
        block = i[7]
        block_code = i[5]
        data = {
            "block": block,
            "block_code": block_code,
            "district": district,
            "name": f"{block}, {district}",
            "state": state,
            "wards": []
        }
        dump_file(data, "lsg")
