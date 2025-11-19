from django.urls import path
from . import views

urlpatterns = [
    # 商品一覧
    path("", views.product_list, name="product_list"),
    
    # カート関連
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    
    # 開発用：顧客切り替え
    path("set-customer/<int:customer_id>/", views.set_customer, name="set_customer"),
]