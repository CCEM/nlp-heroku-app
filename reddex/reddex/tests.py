"""."""
from pyramid import testing
from reddex.views.default import inbound_view
import pytest


@pytest.fixture
def dummy_request():
    """."""
    return testing.DummyRequest()


def test_inbound_returns_dict(dummy_request):
    """."""
    dummy_request.method = 'POST'
    response = inbound_view(dummy_request)
    assert response == {}
