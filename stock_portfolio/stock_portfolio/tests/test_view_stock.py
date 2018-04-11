def test_default_behavior_of_portfolio_view_instance(dummy_request):
    """test portfolio view instance"""
    from ..views.stocks import portfolio_view

    response = portfolio_view(dummy_request)
    assert isinstance(response, dict)
    assert isinstance(response['stocks'], list)


def test_default_behavior_of_portfolio_view(dummy_request):
    """test portfolio view"""
    from ..views.stocks import portfolio_view

    response = portfolio_view(dummy_request)
    assert response['stocks'][0]['symbol'] == 'GE'
    assert 'stocks' in response


def test_detail_view(dummy_request):
    """test detail view"""
    from ..views.stocks import detail_view

    dummy_request.matchdict['symbol'] = 'GE'
    response = detail_view(dummy_request)
    assert response['stock']['symbol'] == 'GE'


def test_detail_view_invalid_symbol(dummy_request):
    """test detail view with invalid symbol"""
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.stocks import detail_view

    dummy_request.matchdict['symbol'] = 'ABC'
    response = detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_detail_view_invalid_key(dummy_request):
    """test detail view with invalid key"""
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.stocks import detail_view

    dummy_request.matchdict['symbo'] = 'ABC'
    response = detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_detail_view_add(dummy_request, db_session, test_stock):
    """ test add stock"""
    from ..views.stocks import detail_view
    db_session.add(test_stock)

    dummy_request.matchdict['symbol'] = 'MU'
    response = detail_view(dummy_request)
    assert response['stock']['symbol'] == 'MU'
    assert type(response['companyName']) is str


def test_default_behavior_of_stock_view(dummy_request):
    """test stock view"""
    from ..views.stocks import add_view

    response = add_view(dummy_request)
    assert isinstance(response, dict)
    assert len(response) == 0


def test_default_behavior_of_stock_view_instance(dummy_request):
    """test stock view instance"""
    from ..views.stocks import add_view

    dummy_request.method = 'GET'
    response = add_view(dummy_request)
    assert isinstance(response, dict)


def test_add_stock(dummy_request, test_stock):
    """test add stock to portfolio"""
    from ..views.stocks import add_view
    from pyramid.httpexceptions import HTTPFound

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
