"""Basic utilities module"""
import requests
import csv
import re
from func_timeout import func_timeout, FunctionTimedOut


def request_ct(url, timer=5, retries=3):
    """
    Performs a get request that provides (somewhat) useful error messages.
    If the request isn't successful within the time interval set in timer (seconds),
    it will retry the request up to retries times.
    If timer is set to -1 it will not timeout (nor it will retry).
    If retries is set to -1 it will retries forever.
    """

    if timer == -1:
        try:
            response = requests.get(url)
        except ImportError:
            raise ImportError(
                "Couldn't retrieve the data, check your search expression or try again later."
            )
        else:
            return response

    if retries == -1:
        while True:
            try:
                response = func_timeout(timer, requests.get, args=(url,))
                break
            except FunctionTimedOut:
                print("TIMEOUT: server didn't respond in time. Retrying... endlessly (◕‿◕)")
                continue
            except ImportError:
                raise ImportError(
                    "Couldn't retrieve the data, check your search expression or try again later."
                )
        return response

    counter = 0
    while counter < retries:
        counter += 1
        try:
            response = func_timeout(timer, requests.get, args=(url,))
            break
        except FunctionTimedOut:
            print("TIMEOUT: server didn't respond in time. Retrying...")
            continue
        except ImportError:
            raise ImportError(
                "Couldn't retrieve the data, check your search expression or try again later."
            )
    else:
        raise ImportError(
            "Couldn't retrieve the data due to server not responding. Please try again later."
        )
    return response


def json_handler(url, timer=5, retries=3):
    """Returns request in JSON (dict) format"""
    return request_ct(url, timer=timer, retries=retries).json()


def csv_handler(url, timer=5, retries=3):
    """Returns request in CSV (list of records) format"""

    response = request_ct(url, timer=timer, retries=retries)
    decoded_content = response.content.decode("utf-8")

    split_by_blank = re.split(r"\n\s*\n", decoded_content)  # Extracts header info
    cr = csv.reader(split_by_blank[1].splitlines(), delimiter=",")
    records = list(cr)

    return records
