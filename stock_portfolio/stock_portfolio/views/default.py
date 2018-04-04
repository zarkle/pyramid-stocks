from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/index.jinja2', request_method='GET')
def get_home_view(request):
    return {}


@view_config(route_name='auth', renderer='../templates/login.jinja2', request_method='GET')
def get_auth_view(request):
    return {}


@view_config(route_name='stock', renderer='../templates/stock-add.jinja2', request_method='GET')
def get_stock_view(request):
    return {}


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2', request_method='GET')
def get_portfolio_view(request):
    return {}

