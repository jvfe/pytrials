========
pytrials
========


.. image:: https://img.shields.io/pypi/v/pytrials.svg
        :target: https://pypi.python.org/pypi/pytrials

.. image:: https://img.shields.io/travis/jvfe/pytrials.svg
        :target: https://travis-ci.com/jvfe/pytrials

.. image:: https://readthedocs.org/projects/pytrials/badge/?version=latest
        :target: https://pytrials.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Python wrapper around the clinicaltrials.gov API.
Documentation for the api can be found here: https://clinicaltrials.gov/api/


* Free software: BSD license
* Documentation: https://pytrials.readthedocs.io.


Tutorial
--------
To install::

    $ pip install pytrials

Basic Usage
^^^^^^^^^^^
::

    from pytrials.client import ClinicalTrials
    
    ct = ClinicalTrials()
    
    # Get 50 full studies related to Coronavirus and COVID in json format.
    ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=50)

    # Get the NCTId, Condition and Brief title fields from 500 studies related to Coronavirus and Covid, in csv format.
    ct.get_study_fields(
        search_expr="Coronavirus+COVID",
        fields=["NCTId", "Condition", "BriefTitle"],
        max_studies=500,
        fmt="csv",
    )

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
