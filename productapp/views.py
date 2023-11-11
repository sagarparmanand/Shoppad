from django.shortcuts import render,HttpResponse,redirect
from productapp.models import Product

# Create your views here.

def homepage(request):
    return HttpResponse("Hello from ProductAPP")

def add_product(request):
    if request.method=='GET':
        print("In Get Method ")
        return render(request,'product/store_product.html')

    else:
        print("In Post Method ")
        
        name=request.POST['pname']
        price=request.POST['price']
        qty=request.POST['qty']
        cat=request.POST['cat']
        is_available=request.POST['avail']

        p=Product.objects.create(name=name,price=price,qty=qty,cat=cat,is_available=is_available)
        # print(p)
        p.save()

        # print("Product Name: ",name)
        # print("Product price: ",price)
        # print("Product qty: ",qty)
        # print("Product category: ",cat)
        # print("Product is available: ",is_available)
        # return HttpResponse("Method is Posted")
        return redirect('/productapp/productdash')
    
def product_dashboard(request):
    context={}
    p=Product.objects.all()
    context['products']=p

    return render(request,'product/productDashboard.html',context)

def delete_product(request,pid):
    p=Product.objects.filter(id=pid)
    p.delete()
    return redirect('/productapp/productdash')

def edit_product(request,pid):
    context={}
    p=Product.objects.filter(id=pid)
    context['products']=p

    return render(request,'product/edit.html',context)