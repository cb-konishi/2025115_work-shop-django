from django.contrib import admin
from .models import Product, Customer, Cart, CartItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """商品管理画面"""
    list_display = ("id", "name", "price")
    search_fields = ("name",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """顧客管理画面"""
    list_display = ['id', 'username', 'email', 'age', 'sex', 'created_at']
    search_fields = ['username', 'email']
    list_filter = ['sex', 'age']
    readonly_fields = ['created_at']


class CartItemInline(admin.TabularInline):
    """カートアイテムのインライン表示"""
    model = CartItem
    extra = 0
    fields = ['product', 'quantity', 'get_subtotal', 'added_at']
    readonly_fields = ['get_subtotal', 'added_at']
    
    def get_subtotal(self, obj):
        """小計の表示"""
        if obj.id:
            return f"¥{obj.get_subtotal()}"
        return "-"
    get_subtotal.short_description = "小計"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """カート管理画面"""
    list_display = ['id', 'customer', 'get_total_quantity', 'get_total_price', 'created_at', 'updated_at']
    search_fields = ['customer__username', 'customer__email']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at', 'get_total_price', 'get_total_quantity']
    inlines = [CartItemInline]
    
    def get_total_price(self, obj):
        """合計金額の表示"""
        return f"¥{obj.get_total_price()}"
    get_total_price.short_description = "合計金額"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """カートアイテム管理画面"""
    list_display = ['id', 'cart', 'product', 'quantity', 'get_subtotal', 'added_at']
    search_fields = ['cart__customer__username', 'product__name']
    list_filter = ['added_at']
    readonly_fields = ['get_subtotal', 'added_at']
    
    def get_subtotal(self, obj):
        """小計の表示"""
        return f"¥{obj.get_subtotal()}"
    get_subtotal.short_description = "小計"