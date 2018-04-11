from pyramid.view import view_config
# from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import requests
import json
from ..models import Stock
from . import DB_ERR_MSG
from sqlalchemy.exc import DBAPIError, IntegrityError

# global constant for base route for API calls to IEX API
API_URL = 'https://api.iextrading.com/1.0'


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
        company = response.json()

        model = Stock(**company)
        try:
            request.dbsession.add(model)
            # request.dbsession.update(model).where(table.symbol=='symbol').value
        except IntegrityError:
            # query = request.dbsession.query(Stock)
            # stock_detail = query.filter(Stock.symbol == symbol).first()
            pass

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()

