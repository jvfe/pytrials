#!/usr/bin/env python

"""Tests for `pytrials` package."""
import pytest
from pytest import raises
from pytrials.client import ClinicalTrials

ct = ClinicalTrials()


def test_full_studies():
    ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=50)


def test_full_studies_max():
    ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=100)


def test_full_studies_below():
    with raises(ValueError):
        ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=-100)


def test_full_studies_above():
    with raises(ValueError):
        ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=150)


def test_study_fields_csv():
    ct.get_study_fields(
        search_expr="Coronavirus+COVID",
        fields=["NCTId", "Condition", "BriefTitle"],
        max_studies=50,
        fmt="csv",
    )


def test_study_fields_json():
    ct.get_study_fields(
        search_expr="Coronavirus+COVID",
        fields=["NCTId", "Condition", "BriefTitle"],
        max_studies=50,
        fmt="json",
    )


def test_study_fake_fields():
    with raises(ValueError) as invalid_field:
        ct.get_study_fields(
            search_expr="Coronavirus+COVID",
            fields=["NCTId", "I AM NOT A REAL FIELD"],
            max_studies=50,
            fmt="json",
        )


def test_study_fake_fmt():
    with raises(ValueError) as invalid_fmt:
        ct.get_study_fields(
            search_expr="Coronavirus+COVID",
            fields=["NCTId", "BriefTitle"],
            max_studies=50,
            fmt="I AM NOT A REAL FORMAT",
        )
