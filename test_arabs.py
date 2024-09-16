from collect_arabs import *
from random import choice
import os
import pytest
import data
from unittest.mock import patch


@pytest.fixture
def mock_input():
    with patch('builtins.input', side_effect=[data.BASE_URL+'&page=12', '1']):
        yield


@pytest.fixture
def mock_bad_input():
    with patch('builtins.input', side_effect=['https://bad_url_idk.com', data.BASE_URL, '2']):
        yield


@pytest.mark.parametrize('input_type, expected_url, expected_pages', data.INPUT_DATA)
def test_get_input(request, input_type, expected_url, expected_pages):
    request.getfixturevalue(input_type)
    url, pages = get_input()
    assert url == expected_url
    assert pages == expected_pages


@pytest.mark.parametrize('url, input_pages, expected_page', data.GET_PAGES_DATA)
def test_get_pages(url, input_pages, expected_page):
    pages = get_pages(url, input_pages)
    assert pages[-1].endswith(expected_page)


browser = driver()


@pytest.mark.parametrize('url, expected_len', data.GET_ADV_DATA)
def test_get_adversitements_urls(url, expected_len):
    urls = get_adversitements_urls(browser, url)
    assert len(urls) == expected_len
    assert choice(urls).endswith('.html')


@pytest.mark.parametrize('page, expected_name', data.GET_NAME_DATA)
def test_get_name(page, expected_name):
    browser.get(page)
    name = get_name(browser)
    assert name == expected_name


@pytest.mark.parametrize('adversitement_url, expected_output', data.PARSE_ADV_DATA)
def test_parse_adversitements(adversitement_url, expected_output):
    parsed = parse_adversitements(browser, adversitement_url)
    assert parsed[0] == expected_output


@pytest.mark.parametrize('data_to_export, filename', data.EXPORT_DATA)
def test_export(data_to_export, filename):
    try:
        export(data_to_export, filename)
        df = pd.read_excel(filename)
        file_content = df.values.tolist()[0]
        file_content[2] = '+' + str(file_content[2])

        assert os.path.exists(filename)
        assert data_to_export[0] == file_content
    finally:
        os.remove(filename)
