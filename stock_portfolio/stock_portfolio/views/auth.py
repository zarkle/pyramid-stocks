from pyramid.view import view_config
# from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
# import requests
# import json
# from ..models import Stock
# from . import DB_ERR_MSG
# from sqlalchemy.exc import DBAPIError, IntegrityError
# import sqlalchemy.exc
# from ..models import dbsession


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
