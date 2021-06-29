from pathlib import Path
from tqdm import tqdm

import argparse
import csv
import json


def get_config(path):
    with open(path, "r", encoding="utf-8") as fd:
        return json.load(fd)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", type=str, required=True, help="The path to config file."
    )

    return parser.parse_args()


def main(args):
    config = get_config(args.config)
    in_file = Path(config["csv"])
    out_file = in_file.with_suffix(".jsonl")

    with in_file.open("r", encoding="utf-8") as fd_in, out_file.open(
        "w", encoding="utf-8"
    ) as fd_out:
        reader = csv.reader(fd_in)
        headers = next(reader)

        for row in tqdm(reader, total=config["total"]):
            assert len(headers) == len(row)

            # convert csv row to a python dictionary
            row_as_dict = {k: v for k, v in zip(headers, row)}

            # initialize fixture data
            data = {
                "model": config["model"],
                "fields": {},
            }

            # add optional primary key if defined
            if "pk" in config:
                data["pk"] = row_as_dict[config["pk"]]

            # copy required fields
            for field_name, meta in config["fields"]["copy"].items():
                # parse meta information
                meta = meta.split(":", 1)
                field_type = meta[0]
                rename_to = x if len(meta) == 2 and (x := meta[1]) else field_name

                # optional values must be transformed to None
                value = row_as_dict[field_name]
                if not value:
                    if field_type == "str":
                        value = ""
                    else:
                        value = None

                # perform type conversion (if necessary)
                if value is not None:
                    if field_type == "int":
                        value = int(float(value))
                    elif field_type == "float":
                        value = float(value)

                # add field
                data["fields"][rename_to] = value

            # dump json object to output file
            fd_out.write(json.dumps(data, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main(parse_args())
