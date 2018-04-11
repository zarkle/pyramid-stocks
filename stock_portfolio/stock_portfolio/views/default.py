from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/index.jinja2', request_method='GET')
def home_view(request):
    """home view"""
    return {}
