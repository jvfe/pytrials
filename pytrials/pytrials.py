"""Main module."""
from utils import json_handler, csv_handler


class ClinicalTrials:
    BASE_URL = "https://clinicaltrials.gov/api/"
    INFO = "info/"
    QUERY = "query/"
    _JSON = "fmt=json"
    _CSV = "fmt=csv"

    def __init__(self):
        self.study_fields = self.__get_study_fields()
        self.api_info = self.__api_info()

    def __get_study_fields(self):
        fields_list = json_handler(
            f"{self.BASE_URL}{self.INFO}study_fields_list?{self._JSON}"
        )
        return fields_list["StudyFields"]["Fields"]

    def __api_info(self):
        last_updated = json_handler(f"{self.BASE_URL}{self.INFO}data_vrs?{self._JSON}")[
            "DataVrs"
        ]
        api_version = json_handler(f"{self.BASE_URL}{self.INFO}api_vrs?{self._JSON}")[
            "APIVrs"
        ]

        return api_version, last_updated

    def get_full_studies(self, search_expr, max_studies=50):
        """Returns all content for a maximum of 100 study records."""
        if max_studies > 100 or max_studies < 1:
            raise ValueError("The number of studies can only be between 1 and 100")

        req = f"full_studies?expr={search_expr}&max_rnk={max_studies}&{self._JSON}"

        full_studies = json_handler(f"{self.BASE_URL}{self.QUERY}{req}")

        return full_studies

    def __repr__(self):
        return f"ClinicalTrials.gov client v{self.api_info[0]}, database last updated {self.api_info[1]}"


ct = ClinicalTrials()
print(ct.get_full_studies(search_expr="heart+attack"))

