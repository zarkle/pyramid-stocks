def test_default_behavior_of_base_view(dummy_request):
    from ..views.default import get_home_view
    from pyramid.response import Response

    request = dummy_request
    response = get_home_view(request)
    assert isinstance(response, Response)
    assert 'Stock Portfolio' in response.text


def test_default_behavior_of_detail_view(dummy_request):
    from ..views.default import get_detail_view

    response = get_detail_view(dummy_request)
    assert type(response) == dict
    assert response['stocks'][0]['symbol'] == 'GE'
