import requests


def test_response_status(url, status_code):
    assert (
        requests.get(url).status_code == status_code
    ), f"status_code страницы {url} не равен {status_code}"
