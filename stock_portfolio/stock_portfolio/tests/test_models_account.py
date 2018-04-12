def test_account_model(db_session):
    """test make a new user account"""
    from ..models import Account

    assert len(db_session.query(Account).all()) == 0
    user = Account(
        username='me',
        password='me',
        email='me@me.com',
    )
    db_session.add(user)
    assert len(db_session.query(Account).all()) == 1


# def test_make_user_no_password(db_session):
#     """test can't make new user with no password"""
#     from ..models import Account
#     import pytest
#     from sqlalchemy.exc import DBAPIError

#     assert len(db_session.query(Account).all()) == 0
#     user = Account(
#         username='me',
#         password=None,
#         email='me@me.com',
#     )
#     with pytest.raises(DBAPIError):
#         db_session.add(user)
#         assert len(db_session.query(Account).all()) == 0
#         assert db_session.query(Account).one_or_none() is None


def test_make_user_no_email(db_session):
    """test can make new user with no email"""
    from ..models import Account

    assert len(db_session.query(Account).all()) == 0
    user = Account(
        username='me',
        password='me',
        email='',
    )
    db_session.add(user)
    assert len(db_session.query(Account).all()) == 1


def test_new_user_in_database(db_session):
    """test new user gets added to database"""
    from ..models import Account

    assert len(db_session.query(Account).all()) == 0
    user = Account(
        username='me',
        password='me',
        email='',
    )
    db_session.add(user)
    query = db_session.query(Account)

    assert query.filter(Account.username == 'me').first()
    assert len(db_session.query(Account).all()) == 1

