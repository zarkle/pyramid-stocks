
def test_default_behavior_of_portfolio_view_instance(dummy_request):
    """test portfolio view instance"""
    from ..views.default import portfolio_view
    response = portfolio_view(dummy_request)
    assert isinstance(response, dict)
    assert isinstance(response['stocks'], list)


def test_default_behavior_of_portfolio_view(dummy_request):
    """test portfolio view"""
    from ..views.default import portfolio_view
    response = portfolio_view(dummy_request)
    assert response['stocks'][0]['symbol'] == 'GE'
    assert 'stocks' in response


def test_detail_view(dummy_request):
    """test detail view"""
    from ..views.default import detail_view
    dummy_request.matchdict['symbol'] = 'GE'
    response = detail_view(dummy_request)
    assert response['stock']['symbol'] == 'GE'


def test_detail_view_invalid_symbol(dummy_request):
    """test detail view with invalid symbol"""
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.default import detail_view
    dummy_request.matchdict['symbol'] = 'ABC'
    response = detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_detail_view_invalid_key(dummy_request):
    """test detail view with invalid key"""
    from pyramid.httpexceptions import HTTPNotFound
    from ..views.default import detail_view
    dummy_request.matchdict['symbo'] = 'ABC'
    response = detail_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_default_behavior_of_stock_view_instance(dummy_request):
    """test stock view instance"""
    from ..views.default import add_view
    dummy_request.method = 'GET'
    response = add_view(dummy_request)
    assert isinstance(response, dict)

