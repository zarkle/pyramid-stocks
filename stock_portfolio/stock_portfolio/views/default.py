from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget



@view_config(
    route_name='home',
    renderer='../templates/index.jinja2',
    request_method='GET',
    permission=NO_PERMISSION_REQUIRED
    )
def home_view(request):
    """home view"""
    return {}
