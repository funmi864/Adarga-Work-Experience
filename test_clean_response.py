import pytest
from web_scraping_production import clean_response

def test_clean_response():
    response = "Jude Bellingham:Line1\nLine2\nLine3- Line4"
    expected = ("Jude Bellingham", "Line1, Line2, Line3Line4")
    assert clean_response(response) == expected

def test_dash():
    response = "Andy Murray:Line1- Line2"
    expected = ("Andy Murray", "Line1Line2")
    assert clean_response(response) == expected

def test_newlines():
    response = "Andy Murray:Line1\nLine2\nLine3"
    expected = ("Andy Murray", "Line1, Line2, Line3")
    assert clean_response(response) == expected

def test_NoReplacement():
    response = "Andy Murray:Line1, Line2"
    expected = ("Andy Murray", "Line1, Line2")
    assert clean_response(response) == expected

def test_clean_response_no_colon():
    response = "Jude BellinghamLine1\nLine2- Line3"
    with pytest.raises(ValueError) as e:
        clean_response(response)
        assert e == "Response does not contain a ':' "