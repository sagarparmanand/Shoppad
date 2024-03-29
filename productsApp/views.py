from django.shortcuts import render,HttpResponse,redirect
from productsApp.models import Product,Cart,Orders,Banner
from django.contrib.auth.models import User
import os,random
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.conf import settings
import razorpay
from django.core.mail import send_mail

# Create your views here.

#                                  Admin
def admin_login(request):
    context = {}
    if request.user.is_superuser:
        return redirect('/dashboard')

    if request.method == 'GET':
        return render(request, 'admin/admin_login.html')

    else:
        uname = request.POST['uname']
        upass = request.POST['upass']
        print(uname)
        print(upass)

        if uname == '' or upass == '':
            context['err'] = "Fields cannot be empty"
            return render(request, 'admin/admin_login.html', context)

        a = authenticate(username=uname, password=upass)

        if a is not None and a.is_superuser:
            login(request, a)
            return redirect('/dashboard')
        else:
            context['err'] = "Invalid Username and Password"
            return render(request, 'admin/admin_login.html', context)

def admin_logout(request):
    logout(request)
    return redirect('/admin')

def cadmin(request):
   if request.user.is_superuser:
        context={}
        d=Product.objects.all().order_by('-id')
        context['data']=d
        o=Orders.objects.all().order_by('-id')
        context['o_data']=o
        #    bd=Banner.objects.all().order_by('-ban_cat')
        #    context['bdata']=bd
        return render(request,'admin/admin.html',context)
   else:
        return redirect('/admin')

def admin_add(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request,'admin/admin_add.html')
        else:
            pname=request.POST['cname']
            cat=request.POST['cat']
            scat=request.POST['scat']
            price=request.POST['price']
            discount=request.POST['discount']
            fp=int(discount) / 100 * int(price)
            fp2=int(int(price) - fp)
            final_price=str(fp2)
            csize=request.POST['csize']
            cdesc=request.POST['cdesc']
            img1 = request.FILES['img1']
            img2 = request.FILES['img2']
            img3 = request.FILES['img3']
            img4 = request.FILES['img4']

            d = Product.objects.create(pname=pname, pcat=cat, subcat=scat, price=price, pdis=discount, fprice=final_price , psize=csize, description=cdesc, img1=img1, img2=img2, img3=img3, img4=img4)
            d.save()
            return redirect('/admin')
    else:
        return redirect('/admin')

def admin_update(request,uid):
    if request.user.is_authenticated:
        context={}
        u=Product.objects.get(id=uid)
        context['udata']=u
        if request.method == 'GET':
            return render(request,'admin/admin_update.html',context)
        else:
            pname=request.POST['cname']
            cat=request.POST['cat']
            scat=request.POST['scat']
            price=request.POST['price']
            discount=request.POST['discount']
            fp=int(discount) / 100 * int(price)
            fp2=int(int(price) - fp)
            final_price=str(fp2)
            csize=request.POST['csize']
            cdesc=request.POST['cdesc']
            # img1 = request.FILES['img1']
            # img2 = request.FILES['img2']
            # img3 = request.FILES['img3']
            # img4 = request.FILES['img4']

            d = Product.objects.filter(id=uid)
            d.update(pname=pname, pcat=cat, subcat=scat, price=price, pdis=discount, fprice=final_price , psize=csize, description=cdesc,)

            dd = Product.objects.get(id=uid)
            if len(request.FILES) != 0:
                if len(dd.img1) > 0 or len(dd.img2) > 0 or len(dd.img3) > 0 or len(dd.img4) > 0:
                    os.remove(dd.img1.path)
                    os.remove(dd.img2.path)
                    os.remove(dd.img3.path)
                    os.remove(dd.img4.path)
                dd.img1 = request.FILES['img1']
                dd.img2 = request.FILES['img2']
                dd.img3 = request.FILES['img3']
                dd.img4 = request.FILES['img4']
            dd.save()

            # d = Product.objects.create(pname=pname, pcat=cat, subcat=scat, price=price, pdis=discount, fprice=final_price , psize=csize, description=cdesc, img1=img1, img2=img2, img3=img3, img4=img4)
            # d.save()
            return redirect('/admin')
    else:
        return redirect('/admin')

def admin_delete(request,did):
    d=Product.objects.get(id=did)
    d.delete()
    d1=d.img1
    d2=d.img2
    d3=d.img3
    d4=d.img4
    
    file_path = os.path.join(settings.MEDIA_ROOT, str(d1))
    file_path1 = os.path.join(settings.MEDIA_ROOT, str(d2))
    file_path2 = os.path.join(settings.MEDIA_ROOT, str(d3))
    file_path3 = os.path.join(settings.MEDIA_ROOT, str(d4))
    os.remove(file_path)
    os.remove(file_path1)
    os.remove(file_path2)
    os.remove(file_path3)
    return redirect('/admin')

#                                    Banner
def admin_ban_add(request):
    if request.method == 'POST':
        bimg=request.FILES['img1']
        bcat=request.POST['bcat']

        b=Banner.objects.create(ban_cat=bcat,ban_img=bimg)
        b.save()
        return redirect('/admin')

def admin_ban_del(request,did):
    d=Banner.objects.filter(id=did)
    d.delete()
    return redirect('/admin')

#                                  Admin End

#                                Products Start


# bd=Banner.objects.all().order_by('-ban_cat')
# context['bdata']=bd

def home(request):
    context={}
    d=Product.objects.all().order_by('-id')
    context['data']=d
    return render(request,'products/index.html',context)


def mens(request):
    context={}
    d=Product.objects.all().order_by('-id')
    context['data']=d
    return render(request,'products/mens.html',context)


def womens(request):
    context={}
    d=Product.objects.all().order_by('-id')
    context['data']=d
    return render(request,'products/womens.html',context)


def kids(request):
    context={}
    d=Product.objects.all().order_by('-id')
    context['data']=d
    return render(request,'products/kids.html',context)


def details(request,vid):
    context={}
    d=Product.objects.all()
    context['data']=d
    v=Product.objects.get(id=vid)
    context['view_data']=v

    return render(request,'products/details.html',context)

def price_range(c,p1,p2):
    q1=Q(pcat=c)
    q2=Q(fprice__range=(p1,p2))
    
    p=Product.objects.filter(q1 & q2)
    return p

def price_250_500(request):
    context={}
    cat=request.GET['cat']
    pr1=request.GET['price1']
    pr2=request.GET['price2']
    result=price_range(cat,pr1,pr2)
    context['data']=result
    if cat == 'Mens':
        return render(request,'products/mens.html',context)
    elif cat == 'Womens':
        return render(request,'products/womens.html',context)
    else:
        return render(request,'products/kids.html',context)   
def price_500_1000(request):
    context={}
    cat=request.GET['cat']
    pr1=request.GET['price1']
    pr2=request.GET['price2']
    result=price_range(cat,pr1,pr2)
    context['data']=result
    if cat == 'Mens':
        return render(request,'products/mens.html',context)
    elif cat == 'Womens':
        return render(request,'products/womens.html',context)
    else:
        return render(request,'products/kids.html',context)
def price_1000_1500(request):
    context={}
    cat=request.GET['cat']
    pr1=request.GET['price1']
    pr2=request.GET['price2']
    result=price_range(cat,pr1,pr2)
    context['data']=result
    if cat == 'Mens':
        return render(request,'products/mens.html',context)
    elif cat == 'Womens':
        return render(request,'products/womens.html',context)
    else:
        return render(request,'products/kids.html',context)
def price_1500_2000(request):
    context={}
    cat=request.GET['cat']
    pr1=request.GET['price1']
    pr2=request.GET['price2']
    result=price_range(cat,pr1,pr2)
    context['data']=result
    if cat == 'Mens':
        return render(request,'products/mens.html',context)
    elif cat == 'Womens':
        return render(request,'products/womens.html',context)
    else:
        return render(request,'products/kids.html',context)
def price_2000_3000(request):
    context={}
    cat=request.GET['cat']
    pr1=request.GET['price1']
    pr2=request.GET['price2']
    result=price_range(cat,pr1,pr2)
    context['data']=result
    if cat == 'Mens':
        return render(request,'products/mens.html',context)
    elif cat == 'Womens':
        return render(request,'products/womens.html',context)
    else:
        return render(request,'products/kids.html',context)

#                                Products end

#                                                Cart Section
def cart(request):
    if request.user.is_authenticated:
        context={}
        c=Cart.objects.filter(u_id=request.user.id)
        total=0
        for x in c:
            total=total+(x.p_id.fprice*x.qty)
            c.update(fprice_tot=total)

        nos=len(c)
        context['q']=nos
        context['amt']=total
        
        context['cdata']=c
        return render(request,'products/cart.html',context)
    else:
        return redirect('/account/login')

def cart_add(request,cid):
    context={}
    d=Product.objects.all()
    context['data']=d
    d=Product.objects.get(id=cid)
    context['view_data']=d
    if request.user.is_authenticated:
        user_id=request.user.id
        p_id=Product.objects.get(id=cid)

        q1=Q(u_id=user_id)
        q2=Q(p_id=cid)
        chek=Cart.objects.filter(q1 & q2)

        if len(chek) == 0:
            if request.method == 'POST':
                siz=request.POST['siz']
            print(siz)
            c=Cart.objects.create(u_id=request.user,p_id=p_id,size=siz)
            c.save()
            context['msg1']="Product added..."
            return render(request,'products/details.html',context)
        else:
            context['msg2']="Product already exist..."
            return render(request,'products/details.html',context)
        
    else:
        return redirect('/account/login')
    
def qty(request,qid):
    qparam = request.GET['q']
    c=Cart.objects.filter(id=qid)

    x=c[0].qty

    if qparam=='pluse':
        x=x+1
    else:
        if x>1:
            x=x-1
    c.update(qty=x)

    return redirect("/cart")
    
def cart_del(request,did):
    d=Cart.objects.get(id=did)
    d.delete()
    return redirect('/cart')

def searching(request):
    context={}
    qparam=request.GET['param']
    q1=Q(pname__icontains=qparam)
    q2=Q(pcat__icontains=qparam)
    q3=Q(subcat__icontains=qparam)
    
    p=Product.objects.filter(q1 | q2 | q3)
    context['sdata']=p

    return render(request,'products/search.html',context)


def ans(val):
    p=Product.objects.filter(subcat__iexact=val)
    return p

def searchinged(request):
    context={}

    qp=request.GET['qp']

    if qp == 'Shirts':
        # p=Product.objects.filter(subcat__iexact=qp)
        p=ans(qp)
        context['sdata']=p
        return render(request,'products/search.html',context)
    elif qp == 'TShirts':
        p=ans(qp)
        context['sdata']=p
        return render(request,'products/search.html',context)
    elif qp == 'Pants':
        p=ans(qp)
        context['sdata']=p
        return render(request,'products/search.html',context)
    elif qp == 'Jeans':
        p=ans(qp)
        context['sdata']=p
        return render(request,'products/search.html',context)
    elif qp == 'Shorts':
        p=ans(qp)
        context['sdata']=p
        return render(request,'products/search.html',context)
    elif qp == 'Sarees':
        p=ans(qp)
        context['sdata']=p
        return render(request,'products/search.html',context)
    elif qp == 'Dress':
        p=ans(qp)
        context['sdata']=p
        return render(request,'products/search.html',context)
    elif qp == 'Gown':
        p=ans(qp)
        context['sdata']=p
        return render(request,'products/search.html',context)
    


#                                             Cart Section End 

def contact(request):
    return render(request,'contact.html')

# def payment(request,pid):
def payment(request):
    context={}
    client = razorpay.Client(auth=("rzp_test_gMY9rLWf2DgPUc", "EoXELuZL7t18dYFwjrzW4jnb"))
    # print(client)
    o=Cart.objects.filter(u_id=request.user.id)
    
    total=0
    for x in o:
        total=total+(x.p_id.fprice*x.qty)

    famt=total*100
    # data = { "amount": famt, "currency": "INR", "receipt": o[0].order_id }
    data = { "amount": famt, "currency": "INR"}
    payment = client.order.create(data=data)
    # print(payment)
    context['payment']=payment
    return render(request,'products/pay.html',context)

# Unique id generater
def generate_orderid():
    n=random.randrange(1000,9999)
    order_id='Sp'+str(n)
    o=Orders.objects.filter(order_id=order_id)

    if len(o)==0:
        return order_id
    else:
        generate_orderid()

def sendmail_user(request):
    context={}
    # Order Details
    oid=generate_orderid()
    c=Cart.objects.filter(u_id=request.user.id)
    for x in c:
        o=Orders.objects.create(order_id=oid,o_sub_cat=str(x.p_id.subcat),o_p_name=x.p_id.pname,u_username=str(x.u_id.username),o_price=x.fprice_tot,qty=x.qty,size=x.size)
        o.save()
        x.delete()
    

    # order_id=request.GET['oid']
    rpayid=request.GET['rpayid']
    roid=request.GET['roid']
    # send mail
    subject="Your Order Placed Successfully"
    # msg="ORDER Details are Oreder Id-"+order_id+" Payment Id-"+rpayid
    msg="Your Order Id - "+oid+", Payment Id-"+rpayid

    mail_not = User.objects.get(id=request.user.id)
    gmail = mail_not.email
    
    send_mail(
    subject,
    msg,
    "parmanandsagar733@gmail.com",             # from@example.com
    [gmail],              #  to@example.com
    fail_silently=False,
    )

    c=Cart.objects.filter(u_id=request.user.id)
    c.delete()
    context['succ']='Thank You'

    return render(request,'products/cart.html',context)

#                                Products end


#                                Account start

def user_login(request):
    return render(request,'accounts/login.html')

def user_register(request):
    return render(request,'accounts/register.html')

#                                Account end

#                           Errors

def page_404(request,exception):
    return render(request,'page_404.html',status=404)