def test_default_behavior_of_base_view(dummy_request):
    """"""
    from ..views.default import get_home_view
    from pyramid.response import Response

    request = dummy_request
    response = get_home_view(request)
    assert isinstance(response, dict)
    assert response == {}


def test_default_behavior_of_portfolio_view(dummy_request):
    """"""
    from ..views.default import get_portfolio_view

    response = get_detail_view(dummy_request)
    assert type(response) == dict
    assert response['stocks'][0]['symbol'] == 'GE'


def test_signin_to_auth_view(dummy_request):
    """"""
    from ..views.default import auth_view

    pass
