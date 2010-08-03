#!/usr/bin/env python
# encoding: utf-8

"""
forms.py
Copyright (c) 2010 MoneyMe Team. All rights reserved.

@author lgavinho
@author danielmartins
"""

from django import forms
from models import Transaction

class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, label=u'Login')
    passwd = forms.CharField(widget=forms.PasswordInput(),
                                label=u'Password')


"""
NewExpenseForm
- The Supplier use this form to input expense for client users.
"""
class NewExpenseForm(forms.Form):
	#TODO Colocar mascara nos campos
	moneyid = forms.CharField(label=u'MoneyID',max_length=10, required=True, widget=forms.TextInput(attrs={'size':'10','maxlength':'10'}), help_text='User client MoneyMe ID.')
	amount = forms.DecimalField(label=u'Amount', decimal_places=2, required=True, help_text='Total expense value.')



