from pytrials.utils import json_handler, csv_handler


class ClinicalTrials:
    """ClinicalTrials API client

    Provides functions to easily access the ClinicalTrials.gov API (https://clinicaltrials.gov/api/) 
    in Python.

    Attributes:
        study_fields: List of all study fields you can use in your query.
        api_info: Tuple containing the API version number and the last time the database was updated.
    """

    BASE_URL = "https://clinicaltrials.gov/api/"
    INFO = "info/"
    QUERY = "query/"
    _JSON = "fmt=json"
    _CSV = "fmt=csv"

    def __init__(self):

        self.study_fields = self.__list_fields()
        self.api_info = self.__api_info()

    def __list_fields(self):
        """Returns the study fields list"""
        fields_list = json_handler(
            f"{self.BASE_URL}{self.INFO}study_fields_list?{self._JSON}"
        )
        return fields_list["StudyFields"]["Fields"]

    def __api_info(self):
        """Returns information about the API"""
        last_updated = json_handler(f"{self.BASE_URL}{self.INFO}data_vrs?{self._JSON}")[
            "DataVrs"
        ]
        api_version = json_handler(f"{self.BASE_URL}{self.INFO}api_vrs?{self._JSON}")[
            "APIVrs"
        ]

        return api_version, last_updated

    def get_full_studies(self, search_expr, max_studies=50):
        """Returns all content for a maximum of 100 study records.
        
        Retrieves information from the full studies endpoint, which gets all study fields. 
        This endpoint can only output JSON (Or not-supported XML) format and does not allow 
        requests for more than 100 studies at once.

        Args:
            search_expr (str): A string containing a search expression as specified by 
                `their documentation <https://clinicaltrials.gov/api/gui/ref/syntax#searchExpr>`_.
            max_studies (int): An integer indicating the maximum number of studies to return.
                Defaults to 50.

        Returns:
            dict: Object containing the information queried with the search expression. 
        
        Raises:
            ValueError: The number of studies can only be between 1 and 100
        """
        if max_studies > 100 or max_studies < 1:
            raise ValueError("The number of studies can only be between 1 and 100")

        req = f"full_studies?expr={search_expr}&max_rnk={max_studies}&{self._JSON}"

        full_studies = json_handler(f"{self.BASE_URL}{self.QUERY}{req}")

        return full_studies

    def get_study_fields(self, search_expr, fields, max_studies=50, fmt="csv"):
        """Returns study content for specified fields
        
        Retrieves information from the study fields endpoint, which acquires specified information 
        from a large (max 1000) studies. To see a list of all possible fields, check the class' 
        study_fields attribute.

        Args:
            search_expr (str): A string containing a search expression as specified by 
                `their documentation <https://clinicaltrials.gov/api/gui/ref/syntax#searchExpr>`_.
            fields (list(str)): A list containing the desired information fields.
            max_studies (int): An integer indicating the maximum number of studies to return.
                Defaults to 50.
            fmt (str): A string indicating the output format, csv or json. Defaults to csv.

        Returns:
            Either a dict, if fmt='json', or a list of records (e.g. a list of lists), if fmt='csv. 
            Both containing the maximum number of study fields queried using the specified search expression.
        
        Raises:
            ValueError: The number of studies can only be between 1 and 1000
            ValueError: One of the fields is not valid! Check the study_fields attribute 
                for a list of valid ones.
            ValueError: Format argument has to be either 'csv' or 'json'
        """
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
