from pyramid.view import view_config
# from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import requests
import json
from ..models import Stock
from . import DB_ERR_MSG
from sqlalchemy.exc import DBAPIError

#global constant for base route for API calls to IEX API
API_URL = 'https://api.iextrading.com/1.0'


@view_config(route_name='home', renderer='../templates/index.jinja2', request_method='GET')
def home_view(request):
    """home view"""
    return {}


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def portfolio_view(request):
    """portfolio view"""
    try:
        query = request.dbsession.query(Stock)
        all_stocks = query.all()
    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

    return {'stocks': all_stocks}


@view_config(route_name='detail', renderer='../templates/stock-detail.jinja2')
def detail_view(request):
    """single stock detail view"""
    try:
        symbol = request.matchdict['symbol']
    except KeyError:
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)
        stock_detail = query.filter(Stock.symbol == symbol).first()
    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

    return {'stock': stock_detail}


@view_config(route_name='auth', renderer='../templates/auth.jinja2')
def auth_view(request):
    """sign-in/sign-up view"""
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

    return HTTPNotFound()  # would only hit this if try to do a PUT or DELETE


@view_config(route_name='stock', renderer='../templates/stock-add.jinja2')
def add_view(request):
    """add stock view"""
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}

        response = requests.get('{}/stock/{}/company'.format(API_URL, symbol))
        try:
            data = response.json()
            return {'company': data}
        except json.decoder.JSONDecodeError:
            return {'err': 'Invalid Symbol'}

    if request.method == 'POST':
        symbol = request.POST['symbol']
        response = requests.get('{}/stock/{}/company'.format(API_URL, symbol))
        MOCK_DATA.append(response.json())
        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()

