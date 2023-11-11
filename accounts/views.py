from django.shortcuts import render , HttpResponse , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from accounts.models import Profile
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
            u=User.objects.create(username=uname,email=uemail)
            u.set_password(upass)
            u.save()

            context['success']="Registered Successfully"
            return render(request,'accounts/register.html',context)


def user_logout(request):
    logout(request)
    return redirect('/')


# User Profile Management

def uesr_profile(request):
    context={}
    if request.method=='GET':
        try:
            p=Profile.objects.get(uid=request.user.id)
            context['udata']=p
            return render(request,'accounts/profile.html',context)
        except:
            context['errmsg']="Please Update Your Profile..."
            return render(request,'accounts/profile.html',context)
    
    else:
        fname=request.POST['fname']
        lname=request.POST['lname']
        uemail=request.POST['uemail']
        umob=request.POST['umob']
        uadd=request.POST['uadd']
        try:
            uimg=request.FILES['uimg']
        except:
            context['errmsg']="Fields cannot be empty..."
            return render(request,'accounts/profile.html',context)

        if fname=='' or lname=='' or uemail=='' or umob=='' or uadd=='' or uimg=='':
            context['errmsg']="Fields cannot be empty..."
            return render(request,'accounts/profile.html',context)
        else:
        
            u=User.objects.filter(id=request.user.id)
            u_obj=User.objects.get(id=request.user.id)
            p=Profile.objects.filter(uid=request.user.id)
            if len(p)==0:
                u.update(first_name=fname,last_name=lname,email=uemail)
                p.create(mobile_no=umob,uimage=uimg,uid=u_obj,uadd=uadd)
                return redirect('/account/profile')
            else:
                u.update(first_name=fname,last_name=lname,email=uemail)
                
                up=Profile.objects.get(uid=request.user.id)
                
                up.mobile_no=request.POST['umob']
                up.uadd=request.POST['uadd']
                if len(request.FILES) != 0:
                    if len(up.uimage) > 0:
                        os.remove(up.uimage.path)
                up.uimage=request.FILES['uimg']
                up.save()
                return redirect('/account/profile')

