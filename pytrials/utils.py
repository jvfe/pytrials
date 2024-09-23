"""Basic utilities module"""
import requests
import csv
import re


def request_ct(url):
    """Performs a get request that provides a (somewhat) useful error message."""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.HTTPError as ex:
        raise ex
    except ImportError:
        raise ImportError(
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

    cr = csv.reader(decoded_content.splitlines(), delimiter=",")
    records = list(cr)

    return records

def enrollment_data(full_studies):
    """Returns a subset dataframe with key columns for enrollment data.
    Store the output of get_full_studies() from pytrials.client and use it as input here"""

    import pandas as pd
    studies_df = pd.DataFrame(full_studies[1:], columns = full_studies[0])

    enrollment_df = studies_df[[
        'NCT Number', 'Study Title', 'Study URL', 'Study Status', 'Enrollment', 'Start Date', 'Completion Date', 'Locations'
        ]]
    
    filtered_df = enrollment_df[enrollment_df['Study Status'].isin(['ACTIVE_NOT_RECRUITING', 'TERMINATED', 'COMPLETED'])]

    return filtered_df