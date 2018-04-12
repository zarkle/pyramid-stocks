def test_default_behavior_of_portfolio_view_instance(dummy_request_auth, add_user):
    """test portfolio view instance"""
    from ..views.stocks import portfolio_view

    response = portfolio_view(dummy_request_auth)
    assert isinstance(response, dict)
    assert isinstance(response['stocks'], list)


def test_default_behavior_of_portfolio_view(dummy_request, add_stock):
    """test portfolio view"""
    from ..views.stocks import portfolio_view
    response = portfolio_view(dummy_request)
    assert response['stocks'][0].symbol == 'MU'
    assert 'stocks' in response


def test_detail_view(dummy_request, add_stock):
    """test detail view"""
    from ..views.stocks import detail_view

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


def test_detail_view_add(dummy_request, db_session, test_stock):
    """ test add stock"""
    from ..views.stocks import detail_view
    db_session.add(test_stock)

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


def test_add_stock(dummy_request):
    """test add stock to portfolio"""
    from ..views.stocks import add_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.method = 'POST'
    dummy_request.POST['symbol'] = 'DIS'
    response = add_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_add_stock_adds_to_database(dummy_request, db_session):
    """test add stock to portfolio adds to database"""
    from ..views.stocks import add_view
    from ..models import Stock

    dummy_request.method = 'POST'
    dummy_request.POST['symbol'] = 'DIS'
    add_view(dummy_request)
    query = db_session.query(Stock)
    first = query.filter(Stock.symbol == 'DIS').first()
    assert first.symbol == 'DIS'
    assert first.companyName == 'The Walt Disney Company'


def test_add_stock_duplicate(dummy_request, db_session, test_stock):
    """test try to add stock already in portfolio"""
    from ..views.stocks import add_view
    from pyramid.httpexceptions import HTTPConflict
    db_session.add(test_stock)

    dummy_request.method = 'POST'
    dummy_request.POST['symbol'] = 'MU'
    response = add_view(dummy_request)
    assert isinstance(response, HTTPConflict)


def test_add_stock_wrong_method(dummy_request, test_stock):
    """test add stock to portfolio"""
    from ..views.stocks import add_view
    from pyramid.httpexceptions import HTTPNotFound

    dummy_request.method = 'PUT'
    response = add_view(dummy_request)
    assert isinstance(response, HTTPNotFound)

