from datetime import datetime
from id_validator import validator
from pathlib import Path

import argparse
import pandas as pd
import random
import generators

NOW = datetime.now()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=str,
        required=True,
        help="The root directory of the MIMIC-IV dataset.",
    )

    return parser.parse_args()


def generate_chinese_name(gender):
    # generate surname
    index = random.randint(0, len(generators.SURNAMES) - 1)
    surname = generators.SURNAMES[index]

    # generate first name (male)
    n_firstname_chars = random.choice([1, 2])
    if gender == "M":
        if n_firstname_chars == 2:
            index = random.randint(0, len(generators.MALE_TWO_CHARS) - 1)
            name = generators.MALE_TWO_CHARS[index]
        else:
            index = random.randint(0, len(generators.MALE_ONE_CHAR) - 1)
            name = generators.MALE_ONE_CHAR[index]
    else:
        if n_firstname_chars == 2:
            index = random.randint(0, len(generators.FEMALE_TWO_CHARS) - 1)
            name = generators.FEMALE_TWO_CHARS[index]
        else:
            index = random.randint(0, len(generators.FEMALE_ONE_CHAR) - 1)
            name = generators.FEMALE_ONE_CHAR[index]

    return surname + name


def generate_national_id(age, gender):
    sex = 1 if gender == "M" else 0
    birth_year = str(NOW.year - age)
    is_valid = False

    while not is_valid:
        _id = validator.fake_id(birthday=birth_year, sex=sex)

        # `validator.fake_id` sometimes generates incorrect birth year
        # also make sure that gender is correctly generated
        if _id[6:10] == birth_year and int(_id[-2]) % 2 == sex:
            is_valid = True

    return _id


def choose_best_year(anchor_year_group: str) -> int:
    start, end = anchor_year_group.split("-")
    start, end = int(start), int(end)

    for year in range(start, end + 1):
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            return year

    return start


def preprocess_patients(root: Path):
    # load admissions table to get patient ethnicity mapping
    df = pd.read_csv(root / "core" / "admissions.csv")
    df["ethnicity"] = df["ethnicity"].str.lower()
    mask = (df["ethnicity"] == "other") | (df["ethnicity"] == "unable to obtain")
    df.loc[mask, "ethnicity"] = "unknown"
    ethnicity_mapping = dict(zip(df["subject_id"], df["ethnicity"]))

    # load patients table
    df = pd.read_csv(root / "core" / "patients.csv")

    # generate fake national ID with the same age as the patient
    df["chosen_anchor_year"] = df["anchor_year_group"].apply(choose_best_year)
    df["real_age"] = NOW.year - df["chosen_anchor_year"] + df["anchor_age"]
    df["national_id"] = df.apply(
        lambda x: generate_national_id(x["real_age"], x["gender"]), axis=1
    )

    # generate random chinese names
    df["name"] = df["gender"].apply(lambda x: generate_chinese_name(x))

    # generate patient ethnicity
    df["ethnicity"] = df["subject_id"].map(
        lambda _id: ethnicity_mapping.get(_id, "unknown")
    )

    # output to csv
    df.to_csv("pp-patients.csv", index=False)


def preprocess_admissions(root: Path):
    # load preprocessed patients csv and get mappings
    df = pd.read_csv("pp-patients.csv")
    _anchor = dict(zip(df["subject_id"], df["anchor_year"]))
    _chosen = dict(zip(df["subject_id"], df["chosen_anchor_year"]))
    _patients = df["subject_id"]

    # load admissions csv and delete rows with subject_id
    # that does not exist in pp-patients
    df = pd.read_csv(root / "core" / "admissions.csv")
    df = df[df["subject_id"].isin(_patients)]

    # convert mappings to auxiliary series
    _anchor = df["subject_id"].apply(lambda x: _anchor[x])
    _chosen = df["subject_id"].apply(lambda x: _chosen[x])

    def adjust_year(series):
        _years = series.str.split("-").str[0].astype("float")
        _real_year = (_years - _anchor + _chosen).apply(lambda x: f"{x:.0f}")
        return _real_year + series.str.slice(start=4)

    # adjust admit, discharge, and death times
    df["admittime"] = adjust_year(df["admittime"])
    df["dischtime"] = adjust_year(df["dischtime"])
    df["deathtime"] = adjust_year(df["deathtime"])
    df["edregtime"] = adjust_year(df["edregtime"])
    df["edouttime"] = adjust_year(df["edouttime"])

    # there will be invalid dates (e.g. 2017-02-29)
    # so patients with these admission dates are simply deleted :)
    is_invalid = (
        pd.to_datetime(df["admittime"], errors="coerce").isna()
        | pd.to_datetime(df["dischtime"], errors="coerce").isna()
        | (
            ~df["deathtime"].isna()
            & pd.to_datetime(df["deathtime"], errors="coerce").isna()
        )
        | (
            ~df["edregtime"].isna()
            & pd.to_datetime(df["edregtime"], errors="coerce").isna()
        )
        | (
            ~df["edouttime"].isna()
            & pd.to_datetime(df["edouttime"], errors="coerce").isna()
        )
    )
    tbd_patient_subject_ids = df.loc[is_invalid, "subject_id"]
    df = df[~df["subject_id"].isin(tbd_patient_subject_ids)]

    # transform admission type and marital status
    df["admission_type"] = df["admission_type"].str.lower()
    df["marital_status"] = df["marital_status"].str.lower()

    # output to csv
    df.to_csv("pp-admissions.csv", index=False)

    # read pp-patients.csv to delete unwanted patients
    df = pd.read_csv("pp-patients.csv")
    df = df[~df["subject_id"].isin(tbd_patient_subject_ids)]
    df.to_csv("pp-patients.csv", index=False)


def preprocess_icustays(root: Path):
    # load preprocessed patients csv and get mappings
    df = pd.read_csv("pp-patients.csv")
    _anchor = dict(zip(df["subject_id"], df["anchor_year"]))
    _chosen = dict(zip(df["subject_id"], df["chosen_anchor_year"]))
    _patients = df["subject_id"]

    # load admissions csv and delete rows with subject_id
    # that does not exist in pp-patients
    df = pd.read_csv(root / "icu" / "icustays.csv")
    df = df[df["subject_id"].isin(_patients)]

    # convert mappings to auxiliary series
    _anchor = df["subject_id"].apply(lambda x: _anchor[x])
    _chosen = df["subject_id"].apply(lambda x: _chosen[x])

    def adjust_year(series):
        _years = series.str.split("-").str[0].astype("float")
        _real_year = (_years - _anchor + _chosen).apply(lambda x: f"{x:.0f}")
        return _real_year + series.str.slice(start=4)

    # adjust in and out times
    df["intime"] = adjust_year(df["intime"])
    df["outtime"] = adjust_year(df["outtime"])

    # there will be invalid dates (e.g. 2017-02-29)
    # so patients with these admission dates are simply deleted :)
    is_invalid = (
        pd.to_datetime(df["intime"], errors="coerce").isna()
        | pd.to_datetime(df["outtime"], errors="coerce").isna()
    )
    tbd_patient_subject_ids = df.loc[is_invalid, "subject_id"]
    df = df[~df["subject_id"].isin(tbd_patient_subject_ids)]

    # output to csv
    df.to_csv("pp-icustays.csv", index=False)

    # read pp-patients.csv to delete unwanted patients
    df = pd.read_csv("pp-patients.csv")
    df = df[~df["subject_id"].isin(tbd_patient_subject_ids)]
    df.to_csv("pp-patients.csv", index=False)

    # read pp-admissions.csv to delete unwanted patients
    df = pd.read_csv("pp-admissions.csv")
    df = df[~df["subject_id"].isin(tbd_patient_subject_ids)]
    df.to_csv("pp-admissions.csv", index=False)


def main(args):
    # set MIMIC-IV dataset root path
    root = Path(args.root).expanduser()
    assert root.is_dir()

    # generate realistic national IDs for all patients (wrt. gender, dob)
    # random chinese names are also given for all of the patients
    # preprocess_patients(root)

    # adjust shifted dates of all the admissions
    # and icustays (wrt. patient's anchor year)
    preprocess_admissions(root)
    preprocess_icustays(root)


if __name__ == "__main__":
    main(parse_args())
