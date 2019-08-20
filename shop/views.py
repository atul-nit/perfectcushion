from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Category, Product

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))
    # return HttpResponse("this is index view")


def category(request):
    template = loader.get_template('shop/category.html')
    return HttpResponse(template.render({}, request))

# Category view
def allProdCat(request, c_slug=None):
    c_page = None
    products = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products = Product.objects.filter(category=c_page, available=True)
    else:
        products = Product.objects.all().filter(available=True)
    return render(request, 'shop/category.html', {'category':c_page, 'products':products})


# Product View

def product(request, prod_id):
    product_info = get_object_or_404(Product, id=prod_id)
    # return render(request, 'shop/product.html', {'product': product_info})
    return render(request, 'shop/product_new.html', {'product': product_info})

def ProdCatDetail(request, c_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'shop/product.html', {'product': product})



