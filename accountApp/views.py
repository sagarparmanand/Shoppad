from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
import os

# Create your views here.

def user_login(request):
    
    if request.method=='GET':
        return render(request,'accounts/login.html')

    else:
        context={}
        uname=request.POST['uname']
        upass=request.POST['upass']

        if uname=='' or upass=='':
            context['errmsg']="Fields cannot be empty"
            return render(request,'accounts/login.html',context)
        
        else:
            u=authenticate(username=uname,password=upass)
            # print(u)
            if u is not None:
                login(request,u)
                return redirect('/')

            else:
                context['errmsg']="Invalid Username and Password"
                return render(request,'accounts/login.html',context)

            # return HttpResponse("User Data")-0
        

def user_register(request):

    if request.method=='GET':
        return render(request,'accounts/register.html')
    
    else:
        context={}
        uname=request.POST['uname']
        uemail=request.POST['uemail']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']

        if uname=='' or uemail=='' or upass=='' or ucpass=='':
            context['errmsg']="Fields cannot be empty"
            return render(request,'accounts/register.html',context)

        elif upass!=ucpass:
            context['errmsg']="Password and Confirm Password Mismatched"
            return render(request,'accounts/register.html',context)
        
        elif len(upass)<8:
            context['errmsg']="Password should be 8 character"
            return render(request,'accounts/register.html',context)

        elif upass.isdigit():
            context['errmsg']="Password should not be entirly in digit"
            return render(request,'accounts/register.html',context)
    
        else:
            check=User.objects.filter(username=uname)
            if len(check) == 0:
                u=User.objects.create(username=uname,email=uemail)
                u.set_password(upass)
                u.save()

                context['success']="Registered Successfully"
                return render(request,'accounts/register.html',context)
            else:
                context['errmsg']="Username already taken..."
                return render(request,'accounts/register.html',context)


def user_logout(request):
    logout(request)
    return redirect('/')

def user_forget(request):
    context = {}
    if request.method == 'GET':
        return render(request,'accounts/forgot.html')
    
    else:
        uname = request.POST['uname']
        upass = request.POST['upass']

        if uname == '' or upass == '':
            context['errmsg'] = 'username and password cannot be empty..'
            return render(request,'accounts/forgot.html',context)
        
        try:
            u=User.objects.get(username=uname)
        except User.DoesNotExist:
            context['errmsg'] = 'User does not exist.'
            return render(request,'accounts/forgot.html',context)
        
        u.set_password(upass)
        u.save()
        return redirect('/account/login')