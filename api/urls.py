'''
Created on Jul 28, 2010

@author: daniel
'''

from django.conf.urls.defaults import *
from piston.resource import Resource
from api.handlers import TransactionHandler

transaction_resource = Resource(TransactionHandler)

urlpatterns = patterns('',
    url(r'transactions/(?P<id>\d+)$', transaction_resource),
    url(r'transactions$', transaction_resource)
)
