from os import listdir
import csv

# {
#     "LSG_CODE": [
#         {
#             "ward_id": "Ward Code",
#             "ward_name": "Ward Name",
#             "ward_no": "Ward Number"
#         },
#     ]
# }

CSV_FOLDER = "csv_files"
list_of_csv_files = listdir(CSV_FOLDER)


def load_all_ward_data():
    ward_data = {}
    for file in list_of_csv_files:
        with open(f"{CSV_FOLDER}/{file}", "r") as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                row_details = {k.strip(): v for k, v in row.items()}
                lsg_code = row_details.get("Local Body Code", "")
                ward = {
                    "ward_no": row_details.get("Ward\nNumber", "") or row_details.get("Ward Number", ""),
                    "ward_name": row_details.get("Ward Name\n(In English)\n", "") or row_details.get("Ward Name (In English)", "") or row_details.get("Ward Name", ""),
                    "ward_id": row_details.get("Ward Code", "")
                }
                if lsg_code in ward_data:
                    ward_data[lsg_code] += [ward]
                else:
                    ward_data[lsg_code] = [ward]
    return ward_data
