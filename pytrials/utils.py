import requests
import csv


def json_handler(url):

    try:
        response = requests.get(url).json()
    except IOError:
        print(
            "Couldn't retrieve the data, check your search expression or try again later."
        )
    else:
        return response


def csv_handler(url):

    # https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv

    try:
        response = requests.get(url)
    except IOError:
        print(
            "Couldn't retrieve the data, check your search expression or try again later."
        )
    else:
        decoded_content = response.content.decode("utf-8")
        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        records = list(cr)[10:]  # Skips header info

        return records


# import pandas as pd

# df = pd.DataFrame.from_records(my_list[1:], columns=my_list[0])
# print(df)
