from itertools import product
from time import sleep
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Min, Max
from django.http import JsonResponse
from django.template.loader import render_to_string
from cart.cart import Cart
from ecom_app.models import Banner, Category, Main_Category, Product
from django.shortcuts import render, get_object_or_404, redirect

from ecom_app.templatetags.product_tags import calc_sell_price


# base page for debugging
def base(request):
    return render(request, 'base.html')


# index page data
def index(request):
    # data for header and footer
    banners = Banner.objects.all()
    All_Main_cate = Main_Category.objects.all()
    All_cat = Category.objects.all()

    All_products = Product.objects.filter(Section__Name='Deal of the day')
    Products = Product.objects.all()
    context = {'banners': banners,
               'All_Main_cate': All_Main_cate,
               'All_cat': All_cat,
               'All_products': All_products,
               'products': Products}
    return render(request, 'main/home.html', context)


# authintication
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'invalid details')
            return redirect('/login/')
    return render(request, 'registration/login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username):
            messages.error(request, 'user with username already exist')
            if User.objects.filter(email=email):
                messages.error(request, 'user with this email already exists')
                return redirect('login')
        else:
            messages.success(request, 'User created')
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('/')
    return render(request, 'registration/login.html')


@login_required(login_url='/login/')
def profile(request):
    # for header and footer data
    All_Main_cate = Main_Category.objects.all()

    context = {'All_Main_cate': All_Main_cate}

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        changepass = request.POST['changepass']
        confirm_changepass = request.POST['confirm_changepass']
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if changepass != "" and confirm_changepass != "" and changepass == confirm_changepass:
            user.set_password(changepass)
        elif changepass != confirm_changepass:
            print('passwords do not match')
            return redirect('/user/profile/')

        user.save()
        messages.success(request, 'changed successfully')
        return redirect('/user/profile/')

    return render(request, 'profile/profile.html', context)


# product logic starts


#
#                             --------------product category---------------
#  no need used ajax filter
# def category(request):
#     category = Category.objects.all()
#     product = Product.objects.all()
#     context = {
#
#         'category': category,
#         'product': product,
#
#     }
#     return render(request, 'Products/all_categories.html')


#                             --------------all product list--------------
def All_products(request):
    # for header and footer data

    All_Main_cate = Main_Category.objects.all()
    category = Category.objects.all()

    min_price = Product.objects.all().aggregate(Min('Price'))
    max_price = Product.objects.all().aggregate(Max('Price'))
    print(min_price)
    print(max_price)

    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(Price__lte=Int_FilterPrice)
    else:
        product = Product.objects.all()
    # main logic starts here
    context = {
        'All_Main_cate': All_Main_cate,
        'category': category,
        'product': product,
        'min_price': min_price,
        'max_price': max_price,
        'FilterPrice': FilterPrice,

    }
    return render(request, 'products/products.html', context)


def wishlist(request):
    # for header and footer data
    All_Main_cate = Main_Category.objects.all()
    All_cat = Category.objects.all()
    # main logic starts here
    return render(request, 'products/wishlist.html')


#                           ----------------detail view  ---------------
def details(request, slug):
    # for header and footer data
    All_Main_cate = Main_Category.objects.all()
    All_cat = Category.objects.all()
    # main logic starts here

    # Products = Product.objects.get(slug=slug)
    Products = get_object_or_404(Product, slug=slug)
    context = {
        'All_Main_cate': All_Main_cate,
        'All_cat': All_cat,
        'All_products': All_products,
        'products': Products
    }
    return render(request, 'Products/product_detail.html', context)
    pass





# order section

def checkout(request):
    return render(request, 'orders/checkout.html')


def my_orders(request):
    return render(request, 'orders/my_orders.html')


# static section
def contact(request):
    return render(request, 'main/contact.html')


def about(request):
    return render(request, 'main/about.html')


def faq(request):
    return render(request, 'main/faq.html')


def custom_404_view(request, exception):
    return render(request, 'Errors/404.html', status=404)


# server side filterin==========================================================================================================================


# filter by category
def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()

    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})


# add to cart logic

@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect('/')


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def category_detail(request,id):
    category = Main_Category.objects.filter(id=id)
    context = {
        'category':category
    }
    return render(request,'Products/category_detail.html',context)


def product_subcategory(request,id):
    category = Category.objects.filter(id=id)
    print(product)
    context = {
        'category':category
    }
    return render(request,'Products/sub_category_details.html',context)