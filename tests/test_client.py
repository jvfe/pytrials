#!/usr/bin/env python

"""Tests for `pytrials` package."""
from pytest import raises
from pytrials.client import ClinicalTrials

ct = ClinicalTrials()


def test_full_studies():
    fifty_studies = ct.get_full_studies(
        search_expr="Coronavirus+COVID", max_studies=50, fmt="json"
    )

    assert [*fifty_studies["studies"][0].keys()] == [
        "protocolSection",
        "derivedSection",
        "hasResults",
    ]

    assert len(fifty_studies["studies"]) == 50


def test_full_studies_max():
    hundred_studies = ct.get_full_studies(
        search_expr="Coronavirus+COVID", max_studies=100, fmt="json"
    )

    assert [*hundred_studies["studies"][0].keys()] == [
        "protocolSection",
        "derivedSection",
        "hasResults",
    ]

    assert len(hundred_studies["studies"]) == 100


def test_full_studies_below():
    with raises(ValueError):
        ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=-100)


def test_full_studies_above():
    with raises(ValueError):
        ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=2000)


def test_study_fields_csv():
    study_fields_csv = ct.get_study_fields(
        search_expr="Coronavirus+COVID",
        fields=["NCT Number", "Conditions", "Study Title"],
        max_studies=50,
        fmt="csv",
    )

    assert len(study_fields_csv) == 51
    assert study_fields_csv[0] == ["NCT Number", "Study Title", "Conditions"]


def test_study_fields_json():
    study_fields_json = ct.get_study_fields(
        search_expr="Coronavirus+COVID",
        fields=["NCTId", "Condition", "BriefTitle"],
        max_studies=50,
        fmt="json",
    )

    assert [
        *study_fields_json["studies"][0]["protocolSection"][
            "identificationModule"
        ].keys()
    ] == [
        "nctId",
        "briefTitle",
    ]

    assert len(study_fields_json["studies"]) == 50


def test_study_fake_fields():
    with raises(ValueError):
        ct.get_study_fields(
            search_expr="Coronavirus+COVID",
            fields=["NCTId", "I AM NOT A REAL FIELD"],
            max_studies=50,
            fmt="json",
        )


def test_study_fake_fmt():
    with raises(ValueError):
        ct.get_study_fields(
            search_expr="Coronavirus+COVID",
            fields=["NCTId", "BriefTitle"],
            max_studies=50,
            fmt="I AM NOT A REAL FORMAT",
        )
