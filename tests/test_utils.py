import pytest
from pytest import raises
from pytrials.utils import request_ct


def test_fake_url():
    with raises(IOError) as exception:
        request_ct("i am a fake url")

