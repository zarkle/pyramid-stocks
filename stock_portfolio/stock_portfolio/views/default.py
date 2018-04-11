from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.httpexceptions import HTTPFound


@view_config(
    route_name='home',
    renderer='../templates/index.jinja2',
    request_method='GET',
    permission=NO_PERMISSION_REQUIRED
    )
def home_view(request):
    """home view"""
    # if request.authenticated_user is not None:
    #     return HTTPFound(location=request.route_url('portfolio'))

    return {}
