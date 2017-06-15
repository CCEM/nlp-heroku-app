"""."""
from pyramid import testing
from reddex.views.default import inbound_api
from datetime import datetime
from reddex.models.meta import Base
from reddex.models import SubReddit
from reddex.models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from reddex.views.default import (
    home_view,
    about_view,
    inbound_api
)
from pyramid.httpexceptions import HTTPNotFound
import webtest
import pytest
import transaction


SAMPLE_POST = {'reddex0': "I hate cake.", 'reddex1': "Dogs are cute."}


@pytest.fixture
def dummy_request(db_session):
    """."""
    dummy_request = testing.DummyRequest()
    dummy_request.dbsession = db_session
    return dummy_request


@pytest.fixture(scope='session')
def db_session(configuration, request):
    """Create a session for interacting with the test database."""
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        import random
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

        session.add_all(holder)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres:///test_reddexdb'
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
        settings['sqlalchemy.url'] = 'postgres:///test_reddexdb'
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

def test_database_fills(db_session):
    """Check database is filled."""
    assert len(db_session.query(SubReddit).all()) == 50


def test_inbound_returns_dict(dummy_request):
    """."""
    dummy_request.method = 'POST'
    dummy_request.POST = SAMPLE_POST
    response = inbound_api(dummy_request)
    assert type(response) is dict


def test_inbound_handles_data(dummy_request):
    """."""
    dummy_request.method = 'POST'
    dummy_request.POST = SAMPLE_POST
    response = inbound_api(dummy_request)
    assert response == {'reddex0': -0.5719, 'reddex1': 0.4588}


def test_home_route_returns_dict(dummy_request):
    """."""
    assert type(home_view(dummy_request)) == dict


def test_about_route_returns_dict(dummy_request):
    """."""
    assert type(about_view(dummy_request)) == dict


def test_inbound_returns_headers(dummy_request):
    """."""
    with pytest.raises(HTTPNotFound):
        inbound_api(dummy_request)


def test_inbound_bad_data(dummy_request):
    """."""
    dummy_request.method = 'POST'
    dummy_request.POST = [1, 2, 3, 4, 5]
    assert inbound_api(dummy_request) == 'Invalid input.'


def test_add_to_db_increase_size(db_session):
    """."""
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


# ++++++++ Functional Tests +++++++++ #
