"""
Test money me expense
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from models import UserProfile



class ACLTest(TestCase):
    # we need fixtures because on run tests is created a db specific for testing
    # and we need the default groups created for testing groups and permissions
    fixtures = ['default_auth2test.json']
    
    def setUp(self):       
        # when create users must be created too the default profiles
        self.usr1 = User.objects.create_user("usr1", "usr1@domain.com", "123")
        self.usr2 = User.objects.create_user("usr2", "usr2@domain.com", "123")
#        self.usr2.groups
    
    def testACLDefaultGroupOfUser(self):
        """
        Tests if the default is correctly applied on create user 
        """
        up = self.usr1.get_profile()
        self.failUnless(isinstance(up, UserProfile), "The default profile is not \
                                                    the default profile class")
        
        try:
            cli = up.user.groups.get(name="Client")
        except ObjectDoesNotExist:
            self.fail("The user must be in the default group[Client] maybe " + 
                      "the signal that create profile on create user is not" + 
                      "correctly configured")    
        
        # the default client must have the permission to confirm an expend
        self.failIf( not self.usr1.has_perm("expense.can_confirm_expend"), "The user" + 
                        "must have the default permission")
        
        # the default client must not havee the permission to insert expend for a client
        # just the Supplier must have this permission
        self.failIf( self.usr1.has_perm("expense.can_insert_expend_for_client"),
                     "The user must not have the permission to insert an "+ 
                     "expend for a client that not be himself")
    
