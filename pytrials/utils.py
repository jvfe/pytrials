"""Basic utilities module"""
import requests
import csv
import re
import json


def request_ct(url):
    """Performs a get request that provides a (somewhat) useful error message."""
    try:
        import urllib.request
        response = urllib.request.urlopen(url.replace(" ", "%20"))
        return response
    except urllib.error.HTTPError as ex:
        raise ex
    except ImportError:
        raise ImportError(
            "Couldn't retrieve the data, check your search expression or try again later."
        )

def json_handler(url):
    """Returns request in JSON (dict) format"""
    response = request_ct(url)
    return json.loads(response.read().decode('utf-8'))


def csv_handler(url):
    """Returns request in CSV (list of records) format"""

    response = request_ct(url)
    decoded_content = response.read().decode("utf-8")

    cr = csv.reader(decoded_content.splitlines(), delimiter=",")
    records = list(cr)

    return records
