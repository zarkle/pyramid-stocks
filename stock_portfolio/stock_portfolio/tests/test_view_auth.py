def test_default_behavior_of_auth_view(dummy_request):
    """test auth view"""
    from ..views.auth import auth_view

    response = auth_view(dummy_request)
    assert isinstance(response, dict)
    assert response == {}


def test_signin_to_auth_view(dummy_request, db_session, test_user):
    """test auth view sign-in"""
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound
    db_session.add(test_user)

    dummy_request.method = 'GET'
    dummy_request.GET = {'username': 'me', 'password': 'me'}
    response = auth_view(dummy_request)
    assert isinstance(response, HTTPFound)


def test_auth_view_sign_up(dummy_request):
    """test auth view sign-up"""
