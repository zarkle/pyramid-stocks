import pytest
import os
from pyramid import testing
from ..models.meta import Base
from ..models import Stock, Account


@pytest.fixture
def test_stock():
    """Set up a test stock"""
    return Stock(
        symbol="MU",
        companyName="Micron Technology Inc.",
        exchange="Nasdaq Global Select",
        industry="Semiconductors",
        website="http://www.micron.com",
        description="Micron Technology Inc along with its subsidiaries provide memory and storage solutions. Its product portfolio consists of memory and storage technologies such as DRAM, NAND, NOR and 3D XPoint memory.",
        CEO="Michael Stewart",
        issueType="cs",
        sector="Technology"
    )


@pytest.fixture
def configuration(request):
    """Setup a database for testing purposes"""
    config = testing.setUp(settings={
        # 'sqlalchemy.url': 'postgres://localhost:5432/stock_app_test'
        'sqlalchemy.url': os.environ['TEST_DATABASE_URL']
    })
    config.include('..models')
    config.include('..routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a database session for interacting with the test database"""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create a dummy request"""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_stock(dummy_request, test_stock):
    """Add a stock to database"""
    dummy_request.dbsession.add(test_stock)
    return test_stock


@pytest.fixture
def test_user():
    """Set up a test user"""
    return Account(
        username="me",
        password="me",
        email="me@me.com",
    )


@pytest.fixture
def add_user(dummy_request, test_user):
    """Add a user to database"""
    dummy_request.dbsession.add(test_user)
    return test_user


# @pytest.fixture
# def auth_config(configuration):
#     configuration.testing_securitypolicy(
#         userid="me", permissive=True
#     )
#     return configuration


# @pytest.fixture
# def db_session_auth(auth_config, request):
#     """Create a database session for interacting with the test database"""
#     SessionFactory = auth_config.registry['dbsession_factory']
#     session = SessionFactory()
#     engine = session.bind
#     Base.metadata.create_all(engine)

#     def teardown():
#         session.transaction.rollback()
#         Base.metadata.drop_all(engine)

#     request.addfinalizer(teardown)
#     return session


# @pytest.fixture
# def dummy_request_auth(db_session_auth):
#     """Create a dummy request"""
#     return testing.DummyRequest(dbsession=db_session_auth)


# @pytest.fixture
# def add_user_auth(dummy_request_auth, test_user):
#     """Add a user to database"""
#     dummy_request_auth.dbsession.add(test_user)
#     return test_user

# {
#     "symbol": "MMM",
#     "companyName": "3M Company",
#     "exchange": "New York Stock Exchange",
#     "industry": "Industrial Products",
#     "website": "http://www.3m.com",
#     "description": "3M Co is a diversified technology company. It manufactures a diverse array of industrial and consumer products. Its business segments are Industrial, Safety and Graphics, Health Care, Electronics and Energy, and Consumer.",
#     "CEO": "Inge G. Thulin",
#     "issueType": "cs",
#     "sector": "Industrials"
# # }

#     dummy_request.POST = {
#         "symbol": "DIS",
#         "companyName": "The Walt Disney Company",
#         "exchange": "New York Stock Exchange",
#         "industry": "Entertainment",
#         "website": "http://www.disney.com",
#         "description": "Walt Disney Co together with its subsidiaries is a diversified worldwide entertainment company with operations in four business segments: Media Networks, Parks and Resorts, Studio Entertainment, and Consumer Products & Interactive Media.",
#         "CEO": "Robert A. Iger",
#         "issueType": "cs",
#         "sector": "Consumer Cyclical"
#     }
