# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

from django.contrib.auth.models import User, Group
from django.db.models import exceptions as model_exceptions
from django.db.models.signals import post_save
from django.db.models import ObjectDoesNotExist

from managers import SubExpendTypeManager


#- TransactionType: income, expend 
TRANSACTION_TYPE_INCOME = 'IN'
TRANSACTION_TYPE_EXPEND = 'EX'
TRANSACTION_TYPE = (
                    (TRANSACTION_TYPE_INCOME, u'Income'),
                    (TRANSACTION_TYPE_EXPEND, u'Expense')
                    )
#- TransactionStatus: approved, not approved, 
TRANSACTION_STATUS_APPROVED = 'OK'
TRANSACTION_STATUS_NOT_APPROVED = 'WT'
TRANSACTION_STATUS = (
                      (TRANSACTION_STATUS_APPROVED, u'Approved'),
                      (TRANSACTION_STATUS_NOT_APPROVED, u'Unapproved')
                      )


#Tipos de despesas. Ex. Supermercado, restaurante e lanchonete, combustíveis, etc.
class ExpendCategory(models.Model):
    """
    # Test behavior -  Not too much to test :P
    >>> a = ExpendType.objects.create(title="Alimentação")
    >>> b = ExpendType.objects.create(title="Fast Food")
    >>> c = ExpendType.objects.create(title="Churrascaria")
    >>> b.parent = a
    >>> c.parent = a
    >>> b.save()
    >>> c.save()
    >>> ExpendType.children.of(a)
    [<ExpendType: Churrascaria>, <ExpendType: Fast Food>]
    >>> d = ExpendType.objects.create(title="Habitação")
    >>> e = ExpendType.objects.create(title="Aluguel")
    >>> e.parent = d
    >>> e.save()
    >>> ExpendType.children.of(a)
    [<ExpendType: Churrascaria>, <ExpendType: Fast Food>]
    >>> ExpendType.children.of(d)
    [<ExpendType: Aluguel>]
    """
    title = models.CharField(u'Título',max_length=100, blank=False, null=False)
    parent = models.ForeignKey('self', null=True)
    objects = models.Manager()
    children = SubExpendTypeManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ('title',)
        verbose_name_plural = "Expense Categories"


#Papel do Fornecedor/Provedor das informações dos gastos
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return unicode(self.user)
    
    def get_groups_name(self):
        names = []
        for g in self.user.groups.all():
            names.append(g.name)
        
        return names
    
    def save(self, force_insert=False, force_update=False):
        """
        Override default method to automatically set a group 
        if not exist one for the user
        Default group for new user is Client
        """
        try:
            self.user.groups.get(name="Client")
        except ObjectDoesNotExist:
            try:
                g = Group.objects.get(name="Client")
                self.user.groups.add(g)               
            except ObjectDoesNotExist:
                raise Exception("App not properly configured, did you run ./manage.py setup ?")
        super(UserProfile, self).save(force_insert, force_update)

def post_save_user(instance, **kwargs):
    """
    Create profile if user not have one
    @param instance is a User instance 
    """
    try:
        p = instance.get_profile()    
    except model_exceptions.ObjectDoesNotExist:
        p = UserProfile()
        p.user = instance
        p.save()
    finally:
        return True
        
post_save.connect(post_save_user, sender=User)
    
#Lançamento de despesas e receitas. 
class Transaction(models.Model):
	transaction_type = models.CharField(u'Type',max_length=2, choices=TRANSACTION_TYPE, default=TRANSACTION_TYPE_EXPEND)
	date = models.DateTimeField(u'Date',default=datetime.now, blank=True, null=False)
	amount = models.DecimalField(u'Amount', max_digits=19, decimal_places=8, blank=False, null=False)
	title = models.CharField(u'Title',max_length=100, blank=True, null=True)
	description = models.TextField(u'Description', blank=True, null=True)
	status = models.CharField(u'Status',max_length=2, choices=TRANSACTION_STATUS, default=TRANSACTION_STATUS_NOT_APPROVED)
	expend_category = models.ForeignKey(ExpendCategory)
	provider = models.ForeignKey(User,related_name="place")
	user = models.ForeignKey(User,related_name="user")
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		ordering = ('transaction_type','date', 'expend_category', 'provider',)
		verbose_name_plural = "Transactions"		
		
#Orçamento das receitas e despesas no mês.    
class TransactionPlanned(models.Model):
    amount = models.DecimalField(u'Amount', max_digits=19, decimal_places=8, blank=False, null=False)
    expend_category = models.ForeignKey(ExpendCategory)
    date = models.DateTimeField(u'Date', blank=False, null=False)
    comment = models.TextField(u'Comment', blank=True, null=True)
    
    class Meta:
        ordering = ('date',)		

