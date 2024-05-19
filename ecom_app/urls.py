from django.urls import path
from ecom_app import views
urlpatterns = [

    path('', views.index, name='index'),

    # product section
    path('product/', views.All_products, name='products'),
    path('product/<slug:slug>/', views.details, name='Product_details'),
    path('category/<int:id>/',views.category_detail,name='cat_details'),
    path('sub_cat/<int:id>/',views.product_subcategory,name='product_subcategory'), #detailview
    #ajax-filter
    path('product/filter-data/', views.filter_data, name="filter-data"),

    # order section
    path('wishlist/', views.wishlist, name='wishlist'),
    # path('my-cart/',views.my_cart,name='my-cart'),
    path('my-orders/', views.my_orders, name='my-orders'),
    path('checkout/', views.checkout, name='checkout'),

    # other pages
    path('about-us/', views.about,name='about'),
    path('contact-us/', views.contact,name='contact'),
    path('faq/', views.faq, name='faq'),

    #cart-section
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),

]