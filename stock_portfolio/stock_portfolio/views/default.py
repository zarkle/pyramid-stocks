from pyramid.view import view_config
from pyramid.response import Response
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound


@view_config(route_name='home', renderer='../templates/base.jinja2', request_method='GET')
def get_home_view(request):
    return {}


@view_config(route_name='auth', renderer='../templates/auth.jinja2')
def auth_view(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Pass: {}'.format(username, password))

            return HTTPFound(location=request.route_url('portfolio'))

        except KeyError:
            return {}

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        print('User: {}, Pass: {}, Email: {}'.format(username, password, email))

        return HTTPFound(location=request.route_url('portfolio'))


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2', request_method='GET')
def get_portfolio_view(request):
    return {
        'stocks': MOCK_DATA
    }


@view_config(route_name='detail', renderer='../templates/stock-detail.jinja2', request_method='GET')
def get_detail_view(request):
    return {}


# @view_config(route_name='add', renderer='../templates/stock-add.jinja2')
# def add_view(request):
#     return {}

