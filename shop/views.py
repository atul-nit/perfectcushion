from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group, User
from .forms import SignUpForm

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))
    # return HttpResponse("this is index view")


def category(request):
    template = loader.get_template('shop/category.html')
    return HttpResponse(template.render({}, request))

# # Category view
# def allProdCat(request, c_slug=None):
#     c_page = None
#     products = None
#     if c_slug != None:
#         c_page = get_object_or_404(Category, slug=c_slug)
#         products = Product.objects.filter(category=c_page, available=True)
#     else:
#         products = Product.objects.all().filter(available=True)
#     return render(request, 'shop/category.html', {'category':c_page, 'products':products})

# Category view
def allProdCat(request, c_slug=None):
    c_page = None
    products_list = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products_list = Product.objects.filter(category=c_page, available=True)
    else:
        products_list = Product.objects.all().filter(available=True)
    paginator = Paginator(products_list, 6)
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, 'shop/category.html', {'category':c_page, 'products':products})



# Product View

def product(request, prod_id):
    product_info = get_object_or_404(Product, id=prod_id)
    # return render(request, 'shop/product.html', {'product': product_info})
    return render(request, 'shop/product_new.html', {'product': product_info})

def ProdCatDetail(request, c_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)
        popular = Product.objects.all().order_by('popularity')[:5]
    except Exception as e:
        raise e
    return render(request, 'shop/product.html', {'product': product, 'popular': popular})

def signupview(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user= User.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def myview(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)


"""
d = {"id": 100, "name": John}
d["name"]
d.get("name", "blah")

"""




