from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPConflict, HTTPBadRequest
import requests
import json
from ..models import Stock, Account
from . import DB_ERR_MSG
from sqlalchemy.exc import DBAPIError, IntegrityError

# global constant for base route for API calls to IEX API
API_URL = 'https://api.iextrading.com/1.0'


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2')
def portfolio_view(request):
    """portfolio view"""
    try:
        query = request.dbsession.query(Account)
        instance = query.filter(Account.username == request.authenticated_userid).first()
        # all_stocks = query.all()
    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)
    if instance:
        return {'stocks': instance.stock_id}
    else:
        return HTTPNotFound()


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
        for each in stock_detail.account_id:
            if each.username == request.authenticated_userid:
                return {'stock': stock_detail}
        return HTTPFound()
    except DBAPIError:
        return Response(DB_ERR_MSG, content_type='text/plain', status=500)


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
        if not all([field in request.POST for field in ['symbol', 'companyName']]):
            raise HTTPBadRequest()
        query = request.dbsession.query(Account)
        instance = query.filter(Account.username == request.authenticated_userid).first()

        query = request.dbsession.query(Stock)
        instance2 = query.filter(Stock.symbol == request.POST['symbol']).first()

        if instance2:
            instance2.account_id.append(instance)
        else:
            model = Stock()
            model.account_id.append(instance)
            model.symbol = request.POST['symbol']
            model.companyName = request.POST['companyName']
            model.exchange = request.POST['exchange']
            model.website = request.POST['website']
            model.CEO = request.POST['CEO']
            model.industry = request.POST['industry']
            model.sector = request.POST['sector']
            model.issueType = request.POST['issueType']
            model.description = request.POST['description']

            try:
                request.dbsession.add(model)
                request.dbsession.flush()
            except IntegrityError:
                return HTTPConflict()

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()  # would only hit this if try to do a PUT or DELETE

