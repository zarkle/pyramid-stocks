def test_stock_model(db_session):
    """test make a new stock"""
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
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
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


# def test_make_user_no_password(db_session):
#     """test can't make new user with no password"""
#     from ..models import Stock
#     import pytest
#     from sqlalchemy.exc import DBAPIError

#     assert len(db_session.query(Stock).all()) == 0
#     user = Stock(
#         username='me',
#         password=None,
#         email='me@me.com',
#     )
#     with pytest.raises(DBAPIError):
#         db_session.add(user)
#         assert len(db_session.query(Stock).all()) == 0
#         assert db_session.query(Stock).one_or_none() is None


def test_make_stock_no_ceo(db_session):
    """test can make new stock with no ceo"""
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        symbol="MU",
        companyName="Micron Technology Inc.",
        exchange="Nasdaq Global Select",
        industry="Semiconductors",
        website="http://www.micron.com",
        description="Micron Technology Inc along with its subsidiaries provide memory and storage solutions. Its product portfolio consists of memory and storage technologies such as DRAM, NAND, NOR and 3D XPoint memory.",
        CEO="",
        issueType="cs",
        sector="Technology"
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_new_stock_in_database(db_session):
    """test new stock gets added to database"""
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    user = Stock(
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
    db_session.add(user)
    query = db_session.query(Stock)
    stock = query.filter(Stock.symbol == 'MU').first()
    assert isinstance(stock, Stock)
    assert len(db_session.query(Stock).all()) == 1

