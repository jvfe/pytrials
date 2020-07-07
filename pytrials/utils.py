import requests
import csv
import re


def request_ct(url):
    try:
        response = requests.get(url)
    except:
        raise IOError(
            "Couldn't retrieve the data, check your search expression or try again later."
        )
    else:
        return response


def json_handler(url):
    return request_ct(url).json()


def csv_handler(url):

    # https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv

    response = request_ct(url)
    decoded_content = response.content.decode("utf-8")
    split_by_blank = re.split("\n\s*\n", decoded_content)  # Divides header info
    cr = csv.reader(split_by_blank[1].splitlines(), delimiter=",")
    records = list(cr)

    return records

