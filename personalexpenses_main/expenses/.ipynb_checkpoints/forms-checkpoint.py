from django.forms import ModelForm
from .models import expense
from django import forms
from django.forms import DateTimeField

# creating the expense entry form
class createexpenseform(ModelForm):
    paymentdate = DateTimeField(widget=forms.widgets.DateTimeInput(format="%Y-%M-%D %H:%M:%S"))
    class Meta:
        model = expense
        fields = ['title','value','details','paymentdate','category']
        
# creating a shotlising fomr
class expenseshortlistform(ModelForm):
    Startdate = DateTimeField(widget=forms.widgets.DateTimeInput(format="%Y-%M-%D %H:%M:%S"))
    Enddate = DateTimeField(widget=forms.widgets.DateTimeInput(format="%Y-%M-%D %H:%M:%S"))
    class Meta:
        model = expense
        fields = ['Startdate','Enddate']