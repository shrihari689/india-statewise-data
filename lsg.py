import requests
import csv
import json
import os
from lsg_ward import load_all_ward_data

LSG_FILE = "https://raw.githubusercontent.com/planemad/india-local-government-directory/master/municipal-directory.csv"


def parameterize(word: str) -> str:
    return word.replace(" ", "_").replace(".", "_").lower().strip()


def create_directories(path):
    if not os.path.exists(path):
        os.makedirs(path)


def dump_file(data, type):
    state = parameterize(data["state"])
    district = parameterize(data["district"])
    lsg_code = parameterize(data["lsg_code"])
    path = f"data/{state}/{district}/{type}"

    create_directories(path)

    with open(f"{path}/{lsg_code}.json", "w") as file:
        file.write(json.dumps(data))
    pass


if __name__ == "__main__":
    file = requests.get(LSG_FILE).text
    csv_file = csv.reader(file.splitlines()[1:], delimiter=",")
    ward_details = load_all_ward_data()
    completed_lsg = set()
    for i in csv_file:
        lsg_code = i[2].title()
        if lsg_code in completed_lsg:
            continue
        ward = ward_details.get(lsg_code, [])
        data = {
            "name": i[3].title(),
            "lsg_code": lsg_code,
            "district": i[8].title(),
            "state": i[1].title(),
            "no_of_wards": len(ward),
            "wards": ward
        }
        dump_file(data, "lsg")
        completed_lsg.add(lsg_code)
