"""Main module."""
from utils import json_handler, csv_handler


class ClinicalTrials:

    BASE_URL = "https://clinicaltrials.gov/api/"
    INFO = "info/"
    QUERY = "query/"
    _JSON = "fmt=json"
    _CSV = "fmt=csv"

    def __init__(self):
        self.study_fields = self.__list_fields()
        self.api_info = self.__api_info()

    def __list_fields(self):
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

    def get_study_fields(self, search_expr, fields, max_studies=50, fmt="csv"):
        if max_studies > 1000 or max_studies < 1:
            raise ValueError("The number of studies can only be between 1 and 1000")
        elif not set(fields).issubset(self.study_fields):
            raise ValueError(
                "One of the fields is not valid! Check the study_fields attribute for a list of valid ones."
            )
        else:
            concat_fields = ",".join(fields)
            req = f"study_fields?expr={search_expr}&max_rnk={max_studies}&fields={concat_fields}"
            if fmt == "csv":
                url = f"{self.BASE_URL}{self.QUERY}{req}&{self._CSV}"
                return csv_handler(url)

            elif fmt == "json":
                url = f"{self.BASE_URL}{self.QUERY}{req}&{self._JSON}"
                return json_handler(url)

            else:
                raise ValueError("Format argument has to be either 'csv' or 'json'")

    def __repr__(self):
        return f"ClinicalTrials.gov client v{self.api_info[0]}, database last updated {self.api_info[1]}"


ct = ClinicalTrials()
# print(ct.study_fields)
# print(ct.get_full_studies(search_expr="heart+attack"))
print(
    ct.get_study_fields(
        search_expr="coronavirus+covid", fields=["NCTId", "BriefSummary"], fmt="csv"
    )
)
