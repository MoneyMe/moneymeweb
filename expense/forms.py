'''
Created on Dec 8, 2009

@author: daniel
'''

from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, label=u'Login')
    passwd = forms.CharField(widget=forms.PasswordInput(),
                                label=u'Password')
