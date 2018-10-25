from streamscrape.utils import get_ip_address


def test_get_ip_address():
    test_url = "https://sing.stanford.edu/site"
    assert "171.67.76.12" == get_ip_address(test_url)
