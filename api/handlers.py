'''
Created on Jul 28, 2010

@author: daniel
'''

from piston.handler import BaseHandler
from piston.utils import rc
from expense.models import Transaction

class TransactionHandler(BaseHandler):
    
    model = Transaction
    
#    def read(self, request, id):
#        try:
#            inst = Transaction.objects.get(id=id)
#            return rc.ALL_OK
#        except Transaction.DoesNotExist:
#            return rc.NOT_HERE
#        except Transaction.MultipleObjectsReturned:
#            return rc.DUPLICATE_ENTRY
#    
#    def create(self, request):
#        pass
#    
#    def update(self, request):
#        pass
#    
#    def delete(self, request):
#        pass

