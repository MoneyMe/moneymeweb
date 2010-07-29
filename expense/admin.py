# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from models import ExpendCategory
from models import Transaction
#from models import MoneyProvider 

class AdminExpendCategory(admin.ModelAdmin):
    list_display = ('title',)
    
class AdminTransaction(admin.ModelAdmin):
    list_display = ('date','expend_category','amount','transaction_type','title',)
    date_hierarchy = 'date'
     
#class AdminMoneyProvider(ModelAdmin):
#    list_display = ('user',)
     
admin.site.register(ExpendCategory,AdminExpendCategory)
admin.site.register(Transaction,AdminTransaction)
#admin.site.register(MoneyProvider)
