def test_default_behavior_of_portfolio_view_instance(dummy_request, add_user):
    """test portfolio view instance"""
    from ..views.stocks import portfolio_view

    response = portfolio_view(dummy_request)
    assert isinstance(response, dict)
    assert isinstance(response['stocks'], list)


def test_default_behavior_of_portfolio_view_not_logged_in(dummy_request):
    """test portfolio view when not logged in"""
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.stocks import portfolio_view

    response = portfolio_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_default_behavior_of_portfolio_view(dummy_request, db_session, test_stock, test_user):
    """test portfolio view"""
    from ..views.stocks import portfolio_view

    test_stock.account_id.append(test_user)
    db_session.add(test_stock)
    db_session.add(test_user)
    response = portfolio_view(dummy_request)
    assert response['stocks'][0].symbol == 'MU'
    assert 'stocks' in response


def test_detail_view(dummy_request, db_session, test_stock, test_user):
    """test detail view"""
    from ..views.stocks import detail_view

    test_stock.account_id.append(test_user)
    db_session.add(test_stock)
    db_session.add(test_user)
    dummy_request.matchdict['symbol'] = 'MU'
    response = detail_view(dummy_request)
    assert response['stock'].symbol == 'MU'


def test_detail_view_invalid_key(dummy_request):
    """test detail view with invalid key"""
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.stocks import detail_view

    dummy_request.matchdict['symbo'] = 'ABC'
    response = detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_detail_view_not_found(dummy_request):
    """test detail view with not found"""
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.stocks import detail_view

    response = detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_detail_view_add(dummy_request, db_session, test_stock, test_user):
    """ test add stock"""
    from ..views.stocks import detail_view

    test_stock.account_id.append(test_user)
    db_session.add(test_stock)
    db_session.add(test_user)
    dummy_request.matchdict['symbol'] = 'MU'
    response = detail_view(dummy_request)
    assert response['stock'].symbol == 'MU'
    assert type(response['stock'].companyName) is str


def test_default_behavior_of_stock_view(dummy_request):
    """test stock view"""
    from ..views.stocks import add_view

    response = add_view(dummy_request)
    assert isinstance(response, dict)
    assert len(response) == 0


def test_search_stock_valid_symbol(dummy_request):
    """test add stock to portfolio"""
    from ..views.stocks import add_view

    dummy_request.GET['symbol'] = 'MMM'
    response = add_view(dummy_request)
    assert response['company']['companyName'] == '3M Company'
    assert isinstance(response, dict)
    assert len(response) == 1


def test_search_stock_invalid_symbol(dummy_request):
    """test add stock to portfolio"""
    from ..views.stocks import add_view

    dummy_request.GET['symbol'] = 'MM'
    response = add_view(dummy_request)
    assert response['err'] == 'Invalid Symbol'
    assert isinstance(response, dict)
    assert len(response) == 1


def test_add_stock(dummy_request, db_session, test_user):
    """test add stock to portfolio"""
    from ..views.stocks import add_view
    from pyramid.httpexceptions import HTTPFound

    db_session.add(test_user)

    dummy_request.method = 'POST'
    dummy_request.POST = {
        "symbol": "DIS",
        "companyName": "The Walt Disney Company",
        "exchange": "New York Stock Exchange",
        "industry": "Entertainment",
        "website": "http://www.disney.com",
        "description": "Walt Disney Co together with its subsidiaries is a diversified worldwide entertainment company with operations in four business segments: Media Networks, Parks and Resorts, Studio Entertainment, and Consumer Products & Interactive Media.",
        "CEO": "Robert A. Iger",
        "issueType": "cs",
        "sector": "Consumer Cyclical"
    }

    response = add_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_add_stock_adds_to_database(dummy_request, db_session, test_user):
    """test add stock to portfolio adds to database"""
    from ..views.stocks import add_view
    from ..models import Stock

    db_session.add(test_user)

    dummy_request.method = 'POST'
    dummy_request.POST = {
        "symbol": "DIS",
        "companyName": "The Walt Disney Company",
        "exchange": "New York Stock Exchange",
        "industry": "Entertainment",
        "website": "http://www.disney.com",
        "description": "Walt Disney Co together with its subsidiaries is a diversified worldwide entertainment company with operations in four business segments: Media Networks, Parks and Resorts, Studio Entertainment, and Consumer Products & Interactive Media.",
        "CEO": "Robert A. Iger",
        "issueType": "cs",
        "sector": "Consumer Cyclical"
    }

    add_view(dummy_request)
    query = db_session.query(Stock)
    first = query.filter(Stock.symbol == 'DIS').first()
    assert first.symbol == 'DIS'
    assert first.companyName == 'The Walt Disney Company'


def test_add_stock_duplicate(dummy_request, db_session, test_user, test_stock):
    """test try to add stock already in portfolio"""
    from ..views.stocks import add_view
    from pyramid.httpexceptions import HTTPFound
    from ..models import Stock

    db_session.add(test_user)
    db_session.add(test_stock)
    assert len(db_session.query(Stock).all()) == 1

    dummy_request.method = 'POST'
    dummy_request.POST = {
        "symbol": "MU",
        "companyName": "Micron Technology Inc.",
        "exchange": "Nasdaq Global Select",
        "industry": "Semiconductors",
        "website": "http://www.micron.com",
        "description": "Micron Technology Inc along with its subsidiaries provide memory and storage solutions. Its product portfolio consists of memory and storage technologies such as DRAM, NAND, NOR and 3D XPoint memory.",
        "CEO": "",
        "issueType": "cs",
        "sector": "Technology"
    }

    response = add_view(dummy_request)
    assert isinstance(response, HTTPFound)
    assert len(db_session.query(Stock).all()) == 1



def test_add_stock_invalid(dummy_request, db_session, test_user):
    """test add stock to portfolio without symbol"""
    from ..views.stocks import add_view
    from pyramid.httpexceptions import HTTPConflict

    db_session.add(test_user)

    dummy_request.method = 'POST'
    dummy_request.POST = {
        "symbol": None,
        "companyName": "The Walt Disney Company",
        "exchange": "New York Stock Exchange",
        "industry": "Entertainment",
        "website": "http://www.disney.com",
        "description": "Walt Disney Co together with its subsidiaries is a diversified worldwide entertainment company with operations in four business segments: Media Networks, Parks and Resorts, Studio Entertainment, and Consumer Products & Interactive Media.",
        "CEO": "Robert A. Iger",
        "issueType": "cs",
        "sector": "Consumer Cyclical"
    }
    response = add_view(dummy_request)
    assert isinstance(response, HTTPConflict)


def test_add_stock_wrong_method(dummy_request, test_stock):
    """test add stock to portfolio"""
    from ..views.stocks import add_view
    from pyramid.httpexceptions import HTTPNotFound

    dummy_request.method = 'PUT'
    response = add_view(dummy_request)
    assert isinstance(response, HTTPNotFound)

