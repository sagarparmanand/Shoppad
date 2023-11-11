from django.shortcuts import render, HttpResponse , redirect
from productapp.models import Product
from storeapp.models import Cart , Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.

def homepage(request):

    # return HttpResponse("hello from home")
    context = {}
    context['msg']="Hello, Good Morning !!"
    context['x']=100
    context['y']=200
    context['data']=[10,20,30,40,50,60]

    return render(request,'home.html',context)


# def contact(request):
    
#     return HttpResponse("hello from contact")

# def about(request):
    
#     return HttpResponse("hello from about")

def edit(request,id):

    return HttpResponse("value is "+id)

def delete(request,id):

    return HttpResponse("deleted is "+id)

def add(request,x,y):
    z=int(x)+int(y)

    return HttpResponse("addition is "+str(z))







def home(request):
    p=Product.objects.filter(is_available=True)
    context={}
    
    context['pdata']=p
    
    return render(request,'storeapp/index.html',context)

def about(request):
    return render(request,'storeapp/about.html')

def contact(request):
    return render(request,'storeapp/contact.html')

def cart(request):
    context={}
    if request.user.is_authenticated:
        c=Cart.objects.filter(uid=request.user.id)

        total=0
        for x in c:
            # print(x.pid.price)
            # print(x.qty)
            # print()
            total=total+(x.pid.price*x.qty)

            # d=x.pid.pdiscount/100
            # t=x.pid.price*d
            # s=x.pid.price-t
        
        nos=len(c)
        context['n']=nos
        context['amt']=total

        # context['saving']=t
        # context['discount']=str(s)

        context['pdata']=c
        
        return render(request,'storeapp/cart.html',context)
    else:
        return redirect('/account/login')



def product_details(request,pid):
    p=Product.objects.get(id=pid)
    context={}
    context['pdata']=p
    d=p.pdiscount/100
    t=p.price*d
    s=p.price-t
    # print(s)
    context['saving']=t
    context['discount']=s
    return render(request,'storeapp/product_details.html',context)

def cart_filter(request,catv):
    q1=Q(cat=catv)
    q2=Q(is_available=True)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['pdata']=p
    return render(request,'storeapp/index.html',context)

def price_range(request):
    min=request.GET['min']
    max=request.GET['max']
    context={}
    p=Product.objects.filter(is_available=True)
    context['pdata']=p

    if not min.isdigit() or not max.isdigit():
        context['errmsg']="amount cannot be a negative or character"
        return render(request,'storeapp/index.html',context)
    elif int(min)<0 or int(max)<0:
        context['errmsg']="amount cannot be in negative"
        return render(request,'storeapp/index.html',context)
    elif int(min)>int(max):
        context['errmsg']="min amount cannot be greater than max amount"
        return render(request,'storeapp/index.html',context)   
    else:
        min=int(min)
        max=int(max)
        q1=Q(price__gte=min)
        q2=Q(price__lte=max)
        q3=Q(is_available=True)
        p=Product.objects.filter(q1 & q2 & q3)
        context['pdata']=p
        return render(request,'storeapp/index.html',context)
    
def sorting(request):
    qparam=request.GET['q']
    context={}
    if qparam=='asc':
        # p=Product.objects.order_by('price').filter(is_available=True)
        x='price'
    else:
        # p=Product.objects.order_by('-price').filter(is_available=True)
        x='-price'

    p=Product.objects.order_by(x).filter(is_available=True)
    context['pdata']=p
    return render(request,'storeapp/index.html',context)

def searching(request):
    x=request.GET['param']
    context={}
    q1=Q(name__icontains=x)
    q2=Q(pdetails__icontains=x)
    q3=Q(is_available=True)
    p=Product.objects.filter(q1 | q2 & q3)
    context['pdata']=p
    return render(request,'storeapp/index.html',context)

def addcart(request,prod_id):
    if request.user.is_authenticated:
        # print("User id ",request.user.id)
        user_id=request.user.id
        # print("Product id ",prod_id)
        pobj=Product.objects.get(id=prod_id)

        q1=Q(uid=user_id)
        q2=Q(pid=prod_id)
        check=Cart.objects.filter(q1 & q2)
        # print(check)

        context={}
        context['pdata']=pobj

        d=pobj.pdiscount/100
        t=pobj.price*d
        s=pobj.price-t
        context['saving']=t
        context['discount']=s

        if len(check):
            context['msg1']="Product Already Added in Cart"
            return render(request,'storeapp/product_details.html',context)
        else:
            c=Cart.objects.create(uid=request.user,pid=pobj)
            c.save()
            context['msg2']="Product Added in Cart"
            return render(request,'storeapp/product_details.html',context)
            
    else:
        return redirect('/account/login')
    
def remove_product(request,rid):
    c=Cart.objects.filter(id=rid)
    c.delete()

    return redirect('/pcart')

def changeqty(request,cid):
    qparam=request.GET['q']
    c=Cart.objects.filter(id=cid)
    # print(c)
    # print(c[0])
    x=c[0].qty

    if qparam=='plus':
        x=x+1
    else:
        if x>1:
            x=x-1
    c.update(qty=x)

    return redirect("/pcart")


# Unique id generater
def generate_orderid():
    n=random.randrange(1000,9999)
    order_id='Ek'+str(n)
    o=Order.objects.filter(order_id=order_id)

    if len(o)==0:
        return order_id
    else:
        generate_orderid()


# Place Order Management
def place_order(request):
    context={}
    if request.user.is_authenticated:
        oid=generate_orderid()
        c=Cart.objects.filter(uid=request.user.id)
        
        for x in c:
            o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
            o.save()
            x.delete()
        
        q1=Q(uid=request.user.id)
        q2=Q(is_completed=False)
        o=Order.objects.filter(q1 & q2)

        nos=len(o)
        total=0
        for x in o:
            total=total+(x.pid.price*x.qty)
        
        
        context['n']=nos
        context['amt']=total
        context['orders']=o

        return render(request,'storeapp/place_order.html',context)
    
def cancel_order(request,cid):
    context={}
    o=Order.objects.filter(id=cid)
    o.delete()

    ord=Order.objects.filter(uid=request.user.id)
    nos=len(ord)
    total=0
    for x in ord:
        total=total+(x.pid.price*x.qty)

    context['n']=nos
    context['amt']=total
    context['orders']=ord
    return render(request,'storeapp/place_order.html',context)

def make_payment(request):
    context={}
    client = razorpay.Client(auth=("rzp_test_gMY9rLWf2DgPUc", "EoXELuZL7t18dYFwjrzW4jnb"))
    # print(client)
    q1=Q(uid=request.user.id)
    q2=Q(is_completed=False)
    o=Order.objects.filter(q1 & q2)
    
    total=0
    for x in o:
        total=total+(x.pid.price*x.qty)

    famt=total*100
    data = { "amount": famt, "currency": "INR", "receipt": o[0].order_id }
    payment = client.order.create(data=data)
    # print(payment)
    context['payment']=payment
    return render(request,'storeapp/pay.html',context)

# Email Management

def sendmail(request):
    order_id=request.GET['oid']
    rpayid=request.GET['rpayid']
    roid=request.GET['roid']

    o=Order.objects.filter(order_id=order_id)
    o.update(is_completed=True)

    # send mail
    subject="EKART Order Placed Successfully"
    msg="ORDER Details are Oreder Id-"+order_id+" Payment Id-"+rpayid
    
    send_mail(
    subject,
    msg,
    "parmanandsagar733@gmail.com",             # from@example.com
    ["parmanandsagarr@gmail.com","ganeshsagar0631@gmail.com"],              #  to@example.com
    fail_silently=False,
    )

    return HttpResponse('Payment')