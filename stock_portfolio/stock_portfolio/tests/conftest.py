import pytest
from pyramid import testing


@pytest.fixture
def dummy_request():
    return testing.DummyRequest()


@pytest.fixture
def dummy_get_request():
    request = testing.DummyRequest()
    request.method = 'GET'
    # request = testing.DummyRequest(method='GET')
