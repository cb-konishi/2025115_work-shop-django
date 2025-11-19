from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from .models import Product, Customer, Cart, CartItem


def product_list(request):
    """商品一覧ページ"""
    products = Product.objects.all()
    
    # セッションから顧客IDを取得（簡易的な実装）
    customer_id = request.session.get('customer_id')
    cart_count = 0
    
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
            cart = Cart.objects.filter(customer=customer).first()
            if cart:
                cart_count = cart.get_total_quantity()
        except Customer.DoesNotExist:
            pass
    
    return render(request, "store/product_list.html", {
        "products": products,
        "cart_count": cart_count
    })


def cart_detail(request):
    """カート詳細ページ"""
    # セッションから顧客IDを取得
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        # 顧客IDがセッションにない場合は空のカートを表示
        return render(request, "store/cart_detail.html", {
            "cart": None,
            "cart_items": [],
            "total_price": 0,
            "total_quantity": 0
        })
    
    try:
        customer = Customer.objects.get(id=customer_id)
        cart = Cart.objects.filter(customer=customer).first()
        
        if cart:
            cart_items = cart.items.select_related('product').all()
            total_price = cart.get_total_price()
            total_quantity = cart.get_total_quantity()
        else:
            cart_items = []
            total_price = 0
            total_quantity = 0
        
        return render(request, "store/cart_detail.html", {
            "cart": cart,
            "cart_items": cart_items,
            "total_price": total_price,
            "total_quantity": total_quantity
        })
    except Customer.DoesNotExist:
        return render(request, "store/cart_detail.html", {
            "cart": None,
            "cart_items": [],
            "total_price": 0,
            "total_quantity": 0
        })


@require_POST
def add_to_cart(request, product_id):
    """カートに商品を追加"""
    # セッションから顧客IDを取得
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        return JsonResponse({
            'success': False,
            'message': '顧客情報が見つかりません'
        }, status=400)
    
    try:
        customer = Customer.objects.get(id=customer_id)
        product = get_object_or_404(Product, id=product_id)
        
        # カートを取得または作成
        cart, created = Cart.objects.get_or_create(customer=customer)
        
        # カートアイテムを取得または作成
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            # すでに存在する場合は数量を増やす
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name}をカートに追加しました',
            'cart_count': cart.get_total_quantity()
        })
    except Customer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '顧客情報が見つかりません'
        }, status=400)


@require_POST
def update_cart_item(request, item_id):
    """カートアイテムの数量を更新"""
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        return JsonResponse({
            'success': False,
            'message': '顧客情報が見つかりません'
        }, status=400)
    
    try:
        customer = Customer.objects.get(id=customer_id)
        cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=customer)
        
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': '数量を更新しました',
                'subtotal': float(cart_item.get_subtotal()),
                'cart_total': float(cart_item.cart.get_total_price()),
                'cart_count': cart_item.cart.get_total_quantity()
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '数量は1以上である必要があります'
            }, status=400)
    except (Customer.DoesNotExist, ValueError):
        return JsonResponse({
            'success': False,
            'message': '無効なリクエストです'
        }, status=400)


@require_POST
def remove_from_cart(request, item_id):
    """カートから商品を削除"""
    customer_id = request.session.get('customer_id')
    
    if not customer_id:
        return JsonResponse({
            'success': False,
            'message': '顧客情報が見つかりません'
        }, status=400)
    
    try:
        customer = Customer.objects.get(id=customer_id)
        cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=customer)
        
        cart = cart_item.cart
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': '商品をカートから削除しました',
            'cart_total': float(cart.get_total_price()),
            'cart_count': cart.get_total_quantity()
        })
    except Customer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '顧客情報が見つかりません'
        }, status=400)


def set_customer(request, customer_id):
    """セッションに顧客IDを設定（開発用）"""
    try:
        customer = Customer.objects.get(id=customer_id)
        request.session['customer_id'] = customer_id
        return redirect('product_list')
    except Customer.DoesNotExist:
        return redirect('product_list')