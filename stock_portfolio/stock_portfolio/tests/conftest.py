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
        'sqlalchemy.url': 'postgres://localhost:5432/stock_app_test'
        # 'sqlalchemy.url': os.environ['TEST_DATABASE_URL']
    })
    config.include('stock_porfolio.models')
    config.include('stock_porfolio.routes')

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
def dummy_request():
    """Create a dummy request"""
    return testing.DummyRequest(dbsession=db_session)


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
# }
