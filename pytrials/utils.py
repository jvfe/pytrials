"""Basic utilities module"""
import requests
import csv
import re


def request_ct(url):
    """Performs a get request that provides a (somewhat) useful error message."""
    try:
        response = requests.get(url)
    except:
        raise IOError(
            "Couldn't retrieve the data, check your search expression or try again later."
        )
    else:
        return response


def json_handler(url):
    """Returns request in JSON (dict) format"""
    return request_ct(url).json()


def csv_handler(url):
    """Returns request in CSV (list of records) format"""

    response = request_ct(url)
    decoded_content = response.content.decode("utf-8")

    split_by_blank = re.split(r"\n\s*\n", decoded_content)  # Extracts header info
    cr = csv.reader(split_by_blank[1].splitlines(), delimiter=",")
    records = list(cr)

    return records
