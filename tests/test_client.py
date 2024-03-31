#!/usr/bin/env python

"""Tests for `pytrials` package."""
from pytest import raises
from pytrials.client import ClinicalTrials

ct = ClinicalTrials()


def test_full_studies():
    fifty_studies = ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=50)

    assert len(fifty_studies) == 1

    fifty_studies = fifty_studies[0]

    assert [*fifty_studies["FullStudiesResponse"].keys()] == [
        "APIVrs",
        "DataVrs",
        "Expression",
        "NStudiesAvail",
        "NStudiesFound",
        "MinRank",
        "MaxRank",
        "NStudiesReturned",
        "FullStudies",
    ]

    assert len(fifty_studies["FullStudiesResponse"]["FullStudies"]) == 50


def test_full_studies_max():
    hundred_studies = ct.get_full_studies(
        search_expr="Coronavirus+COVID", max_studies=100
    )

    assert len(hundred_studies) == 1

    hundred_studies = hundred_studies[0]

    assert [*hundred_studies["FullStudiesResponse"].keys()] == [
        "APIVrs",
        "DataVrs",
        "Expression",
        "NStudiesAvail",
        "NStudiesFound",
        "MinRank",
        "MaxRank",
        "NStudiesReturned",
        "FullStudies",
    ]

    assert len(hundred_studies["FullStudiesResponse"]["FullStudies"]) == 100


def test_full_studies_below():
    with raises(ValueError):
        ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=-100)


def test_full_studies_above():
    hundred_fifty_studies = ct.get_full_studies(
        search_expr="Coronavirus+COVID", max_studies=150
    )

    n = 0
    for r in hundred_fifty_studies:
        n += len(r["FullStudiesResponse"]["FullStudies"])

    assert n == 150


def test_study_fields_csv():
    study_fields_csv = ct.get_study_fields(
        search_expr="Coronavirus+COVID",
        fields=["NCTId", "Condition", "BriefTitle"],
        max_studies=50,
        fmt="csv",
    )

    assert len(study_fields_csv) == 51
    assert study_fields_csv[0] == ["Rank", "NCTId", "Condition", "BriefTitle"]


def test_study_fields_json():
    study_fields_json = ct.get_study_fields(
        search_expr="Coronavirus+COVID",
        fields=["NCTId", "Condition", "BriefTitle"],
        max_studies=50,
        fmt="json",
    )

    assert [*study_fields_json["StudyFieldsResponse"].keys()] == [
        "APIVrs",
        "DataVrs",
        "Expression",
        "NStudiesAvail",
        "NStudiesFound",
        "MinRank",
        "MaxRank",
        "NStudiesReturned",
        "FieldList",
        "StudyFields",
    ]

    assert len(study_fields_json["StudyFieldsResponse"]["StudyFields"]) == 50


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


def test_study_count():
    study_count = ct.get_study_count(search_expr="Coronavirus+COVID")

    assert study_count > 2200
