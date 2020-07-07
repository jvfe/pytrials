import requests
import csv
import re


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
        split_by_blank = re.split('\n\s*\n', decoded_content) # Divides header info
        cr = csv.reader(split_by_blank[1].splitlines(), delimiter=",")
        records = list(cr)

        return records