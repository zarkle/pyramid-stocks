def test_default_behavior_of_home_view(dummy_request):
    """test home view"""
    from ..views.default import home_view

    response = home_view(dummy_request)
    assert isinstance(response, dict)
    assert response == {}

