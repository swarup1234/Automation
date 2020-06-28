from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate 
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import createexpenseform, expenseshortlistform
from .models import expense
from django.core.paginator import Paginator
import datetime as dt
import pandas as pd


# Create your views here.
@login_required 
def expenseshome(request):
    return render(request,'expenses/home.html')


@login_required    
def createexpense(request):
    if request.method == 'GET':
        return render(request,'expenses/createexpense.html',{'form':createexpenseform()})
    else:
        try:
            form = createexpenseform(request.POST)
            newexpense = form.save(commit=False)
            newexpense.user = request.user
            newexpense.save()
            return redirect('expenseshome')
        except ValueError:
            print(request.POST)
            return render(request,'expenses/createexpense.html',{'form':createexpenseform(),'error': "Bad data passed in!!"})
        
        
        
@login_required     
def currentexpenses(request, pagination_k = 1, n=10):
    allexpenses = expense.objects.filter(user=request.user).order_by('-paymentdate')
    maxcount = allexpenses.count
    pagination_list = range(0, len(allexpenses),n)
    allexpenses = allexpenses[((pagination_k-1)*n):(pagination_k+n)]
    return render(request,'expenses/currentexpenses.html',{'expenses':allexpenses, 'pagei':pagination_list, 'n':n, 'maxcount':maxcount})

@login_required     
def currentexpensespage(request, pagination_k = 1, n=10):
    allexpenses = expense.objects.filter(user=request.user).order_by('-paymentdate')
    maxcount = allexpenses.count
    pagination_list = range(0, len(allexpenses),n)
    if pagination_k==0:
        import pandas as pd
        df=pd.DataFrame(list(allexpenses.values('title','details','value','paymentdate','category')))
        df.to_csv('fullpath_file.csv',index=False)
        pagination_k=1
    else:
        import pandas as pd
        df=pd.DataFrame(list(allexpenses.values('title','details','value','paymentdate','category')))
        
        
    allexpenses = allexpenses[((pagination_k//10)*n):(pagination_k+n)]
    #df=pd.DataFrame(list(allexpenses.values('id','title','details','value','paymentdate','category')))
    if len(allexpenses)>0:
        return render(request,'expenses/currentexpenses.html',{'expenses':allexpenses, 'pagei':pagination_list, 'n':n, 'maxcount':maxcount, 'Total':int(sum(df.value))})
    else:
        return redirect('currentexpenses')

# function to return a graph    
def return_graph(df):
    import matplotlib.pyplot as plt
    from io import StringIO
    import numpy as np
    
    fig = plt.figure()
    plt.bar(df.category, df.value)
    plt.ylabel('Expenses')

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    pic = imgdata.getvalue()
    return pic


@login_required     
def monthexpensepage(request,pagination_k=1,n=10):
    if request.method == 'GET':
        return render(request,'expenses/monthexpensepage.html')
    else:
        print(request.POST)
        if 'startdate' in request.POST:
            try:
                allexpenses = expense.objects.filter(user=request.user,paymentdate__range=[request.POST['startdate'], request.POST['enddate']]).order_by('-paymentdate')
                df=pd.DataFrame(list(allexpenses.values('id','title','details','value','paymentdate','category')))
                print(df)
                graphval = return_graph(df)
                
                #print(allexpenses)
                expensepage = Paginator(allexpenses,n)
                if 'page' in request.POST:
                    page_number =  request.POST['page']             
                else:
                    page_number = pagination_k
                expensepage = expensepage.get_page(page_number)
                return render(request,'expenses/monthexpensepage.html',{'df':expensepage, 'startdate':request.POST['startdate'],'enddate':request.POST['enddate'],'Total':sum(df.value),'pagei':[(x//10) + 1 for x in range(1,len(df),n)],'graph':graphval})
                #return(HttpResponse(df.to_html()))
            except:
                print(request.POST)
                return render(request,'expenses/monthexpensepage.html',{'error': "Bad data passed in!!"})
        else:
            return render(request,'expenses/monthexpensepage.html')
            


@login_required 
def viewexpense(request, expense_pk):
    allexpenses = get_object_or_404(expense, pk = expense_pk, user=request.user)
    if request.method == 'GET':
        form = createexpenseform(instance=allexpenses)
        return render(request,'expenses/viewexpense.html',{'expense':allexpenses,'form':form})
    else:
        try:
            form = createexpenseform(request.POST,instance=allexpenses)
            form.save()
            return redirect('currentexpenses')
        except ValueError:
             return render(request,'expenses/viewexpense.html',{'expense':allexpenses,'form':form,'error':'Bad data passed in!'})
            

@login_required 
def deleteexpense(request, expense_pk):
    allexpenses = get_object_or_404(expense, pk = expense_pk, user=request.user)
    print(allexpenses, expense_pk, request.user)
    if request.method == 'POST':
        print(allexpenses)
        allexpenses.delete()
        return redirect('currentexpenses')