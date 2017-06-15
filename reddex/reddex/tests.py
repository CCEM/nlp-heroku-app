"""Testing for reddex."""
from pyramid import testing
from reddex.views.default import inbound_api
from pyramid.config import Configurator
from datetime import datetime
from reddex.models.meta import Base
from reddex.models import SubReddit
from reddex.models import get_tm_session
from reddex.views.default import (
    home_view,
    about_view,
)
from reddex.views.notfound import notfound_view
from pyramid.httpexceptions import HTTPNotFound
from reddex.scripts.sentiment_reddex import evaluate_comments
import pytest
import os
import transaction


SAMPLE_POST = {'reddex0': "I hate cake.", 'reddex1': "Dogs are cute."}


@pytest.fixture
def dummy_request(db_session):
    """Create dummy request with db_session."""
    dummy_request = testing.DummyRequest()
    dummy_request.dbsession = db_session
    return dummy_request


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database."""
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def fill_db(testapp):
    """Fill database."""
    import random
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        test_subs = ['test1', 'test2', 'test3', 'test4', 'test5',
                     'test6', 'test7', 'test8', 'test9', 'test10']
        holder = []
        for sub in test_subs:
            for _ in range(5):
                new_entry = SubReddit(
                    name=sub,
                    mean=random.uniform(-1, 1),
                    median=random.uniform(-1, 1),
                    date=datetime.now()
                )
                holder.append(new_entry)

        dbsession.add_all(holder)

    return dbsession


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance."""
    config = testing.setUp(settings={
        'sqlalchemy.url': os.environ.get('TEST_DATABASE_URL')
    })
    config.include('reddex.models')
    config.include('reddex.routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope="session")
def testapp(request):
    """Create a test application for functional tests."""
    from webtest import TestApp

    def main(global_config, **settings):
        """Return a Pyramid WSGI application."""
        settings['sqlalchemy.url'] = os.environ.get('TEST_DATABASE_URL')
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('reddex.models')
        config.include('reddex.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return testapp


# ++++++++ Unit Tests +++++++++ #

def test_database_fills(fill_db, db_session):
    """Check database is filled."""
    assert len(db_session.query(SubReddit).all()) == 50


def test_inbound_returns_dict(dummy_request):
    """Inbound request returns dict."""
    dummy_request.method = 'POST'
    dummy_request.POST = SAMPLE_POST
    response = inbound_api(dummy_request)
    assert type(response) is dict


def test_inbound_handles_data(dummy_request):
    """Inbound request returns accurate data."""
    dummy_request.method = 'POST'
    dummy_request.POST = SAMPLE_POST
    response = inbound_api(dummy_request)
    assert response == {'reddex0': -0.5719, 'reddex1': 0.4588}


def test_home_route_returns_dict(dummy_request):
    """Home view request returns dict."""
    assert type(home_view(dummy_request)) == dict


def test_about_route_returns_dict(dummy_request):
    """About view request returns dict."""
    assert type(about_view(dummy_request)) == dict


def test_bad_inbound_returns_404(dummy_request):
    """Non POST method returns not found object."""
    with pytest.raises(HTTPNotFound):
        inbound_api(dummy_request)


def test_bad_about_returns_404(dummy_request):
    """Non GET method returns not found object."""
    dummy_request.method = 'POST'
    with pytest.raises(HTTPNotFound):
        about_view(dummy_request)


def test_inbound_bad_data(dummy_request):
    """Inbound POST with bad data returns message."""
    dummy_request.method = 'POST'
    dummy_request.POST = [1, 2, 3, 4, 5]
    assert inbound_api(dummy_request) == 'Invalid input.'


def test_add_to_db_increase_size(db_session):
    """Adding one record increases size of db and goes to end."""
    db_len = len(db_session.query(SubReddit).all())
    entry = SubReddit(
        name='metroid',
        mean=0.9,
        median=0.85,
        date=datetime.now()
    )
    db_session.add(entry)
    assert (db_session.query(SubReddit).all())[-1].name == 'metroid'
    assert len(db_session.query(SubReddit).all()) == db_len + 1


def test_notfound_view_returns_dict(dummy_request):
    """404 works."""
    assert notfound_view(dummy_request) == {}


def test_our_vader_integration():
    """Return  neg/pos test score from text."""
    assert evaluate_comments("I love cats!") > 0


def test_our_vader_integration_works_with_empty_string():
    """Return neg/pos test score from text."""
    assert evaluate_comments("") == 0


# ++++++++ Functional Tests +++++++++ #


def test_home_view_returns_200(testapp, db_session, fill_db):
    """Test that the home view returns 200 OK response."""
    response = testapp.get('/')
    assert response.status_code == 200


def test_home_view_returns_some_html(testapp, db_session, fill_db):
    """Home view returns html."""
    response = testapp.get('/')
    assert 'Five most positive subreddits visited by our users' in response.html.text


def test_about_view_returns_200(testapp, db_session, fill_db):
    """Test that the about view returns 200 OK response."""
    response = testapp.get('/about')
    assert response.status_code == 200


def test_about_view_returns_some_html(testapp, db_session, fill_db):
    """About view returns html."""
    response = testapp.get('/about')
    assert 'About the Reddex team' in response.html.text


def test_access_control_header_added_to_request(testapp, db_session, fill_db):
    """Check for access control header."""
    response = testapp.post('/inbound', params=SAMPLE_POST)
    assert 'Access-Control-Allow-Origin' in response.headers
