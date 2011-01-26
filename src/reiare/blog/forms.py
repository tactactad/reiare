# -*- coding: utf-8 -*-
#from django import newforms as forms
from django import forms
from django.forms.fields import *
from django.forms.widgets import *

class CommentForm(forms.Form):
    author = CharField(label='おなまえ', widget=TextInput(attrs={'size': 30}), max_length=50)
    body = CharField(label='こめんと', widget=Textarea(attrs={'rows': 7, 'cols': 40}))

class SearchForm(forms.Form):
    keyword = CharField(label='けんさく', widget=TextInput(attrs={'size': 10}))

