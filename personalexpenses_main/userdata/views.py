from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate 
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'userdata/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request,'userdata/signupuser.html',{'form':UserCreationForm()})
    else:
        # Creating a user
        print("Trying to create User"+str(request.POST['username']))
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request,'userdata/signupuser.html',{'form':UserCreationForm(), 'error': 'Username already taken, please choose another username!'})
        else:
            # tell the user passwords didn't match 
            print("passwords dont match!")
            return render(request,'userdata/signupuser.html',{'form':UserCreationForm(), 'error': 'Passwords didnot match'})
        
        
def changepassworduser(request,username_pk):
    if request.method == 'GET':
        return render(request,'userdata/changepass.html',{'form':SetPasswordForm(user="1"), "username_pk":'1'})
    else:
        # Creating a user
        if 'new_password1' not in request.POST:
            #print(request.POST['username'])
            uname = request.POST['username']
            return render(request,'userdata/changepass.html',{'form':SetPasswordForm(user=uname),'username_pk':uname})
        else:
            if request.POST['new_password1']==request.POST['new_password2']:
                try:
                    print(username_pk)
                    user = User.objects.get(username=request.POST['username'])
                    user.set_password(request.POST['new_password1'])
                    user.save()
                    return redirect('loginuser')
                except:
                    return render(request,'userdata/changepass.html',{'form':SetPasswordForm(user=username_pk), 'error': 'Username is not present! please choose the correct username!',"username_pk":username_pk})
            else:
                # tell the user passwords didn't match 
                print("passwords dont match!")
                return render(request,'userdata/changepass.html',{'form':SetPasswordForm(user=username_pk), 'error': 'Passwords didnot match',"username_pk":username_pk})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
    
def loginuser(request):
    if request.method == 'GET':
        return render(request,'userdata/loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'userdata/loginuser.html',{'form':AuthenticationForm(), 'error':'Username and password did not match!'})
        else:
            login(request, user)
            return redirect('home')
            