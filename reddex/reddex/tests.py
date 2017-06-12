"""."""
from pyramid import testing
from reddex.views.default import inbound_view
import pytest

SAMPLE_POST = {'reddex0': "I hate cake.", 'reddex1': "Dogs are cute."}


@pytest.fixture
def dummy_request():
    """."""
    return testing.DummyRequest()


def test_inbound_returns_dict(dummy_request):
    """."""
    dummy_request.method = 'POST'
    response = inbound_view(dummy_request)
    assert type(response) is dict


def test_inbound_handles_data(dummy_request):
    """."""
    dummy_request.method = 'POST'
    dummy_request.POST = SAMPLE_POST
    response = inbound_view(dummy_request)
    assert response == {'reddex0': -0.5719, 'reddex1': 0.4588}
