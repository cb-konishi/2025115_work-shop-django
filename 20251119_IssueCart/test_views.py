"""
カート機能のビューテスト

Issue: カートに入れる機能実装
日付: 2025-11-19

このテストファイルでは以下をテストします：
1. 商品一覧ページの表示
2. カートへの商品追加API
3. カートアイテムの数量更新API
4. カートからの商品削除API
5. カート詳細ページの表示
"""

import unittest
import json
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product, Customer, Cart, CartItem


class ProductListViewTest(TestCase):
    """商品一覧ビューのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        
        # テスト用の商品を作成
        self.product1 = Product.objects.create(name='商品A', price=Decimal('1000.00'))
        self.product2 = Product.objects.create(name='商品B', price=Decimal('2000.00'))
    
    def test_product_list_view_status_code(self):
        """商品一覧ページが正しく表示されることをテスト"""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_product_list_view_template(self):
        """正しいテンプレートが使用されることをテスト"""
        response = self.client.get(reverse('product_list'))
        self.assertTemplateUsed(response, 'store/product_list.html')
    
    def test_product_list_view_context(self):
        """商品データがコンテキストに含まれることをテスト"""
        response = self.client.get(reverse('product_list'))
        self.assertIn('products', response.context)
        self.assertEqual(len(response.context['products']), 2)
    
    def test_product_list_with_customer_session(self):
        """顧客セッションがある場合のカート数表示テスト"""
        # 顧客とカートを作成
        customer = Customer.objects.create(
            username='test_user',
            age=25,
            email='test@example.com',
            sex='M'
        )
        cart = Cart.objects.create(customer=customer)
        CartItem.objects.create(cart=cart, product=self.product1, quantity=3)
        
        # セッションに顧客IDを設定
        session = self.client.session
        session['customer_id'] = customer.id
        session.save()
        
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.context['cart_count'], 3)


class AddToCartViewTest(TestCase):
    """カート追加ビューのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        
        self.customer = Customer.objects.create(
            username='cart_user',
            age=30,
            email='cart@example.com',
            sex='F'
        )
        
        self.product = Product.objects.create(
            name='テスト商品',
            price=Decimal('1500.00')
        )
        
        # セッションに顧客IDを設定
        session = self.client.session
        session['customer_id'] = self.customer.id
        session.save()
    
    def test_add_to_cart_creates_cart(self):
        """カートがない場合に新規作成されることをテスト"""
        url = reverse('add_to_cart', args=[self.product.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # カートが作成されたことを確認
        self.assertTrue(Cart.objects.filter(customer=self.customer).exists())
    
    def test_add_to_cart_creates_cart_item(self):
        """商品がカートアイテムとして追加されることをテスト"""
        url = reverse('add_to_cart', args=[self.product.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        
        # カートアイテムが作成されたことを確認
        cart = Cart.objects.get(customer=self.customer)
        self.assertTrue(CartItem.objects.filter(cart=cart, product=self.product).exists())
    
    def test_add_to_cart_increases_quantity(self):
        """既存の商品を追加すると数量が増えることをテスト"""
        # 最初に追加
        cart = Cart.objects.create(customer=self.customer)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        
        # 2回目の追加
        url = reverse('add_to_cart', args=[self.product.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        
        # 数量が2になったことを確認
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)
    
    def test_add_to_cart_without_customer_session(self):
        """顧客セッションがない場合はエラーになることをテスト"""
        # セッションをクリア
        self.client.session.flush()
        
        url = reverse('add_to_cart', args=[self.product.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
    
    def test_add_to_cart_returns_cart_count(self):
        """レスポンスにカート数が含まれることをテスト"""
        url = reverse('add_to_cart', args=[self.product.id])
        response = self.client.post(url)
        
        data = response.json()
        self.assertIn('cart_count', data)
        self.assertEqual(data['cart_count'], 1)


class UpdateCartItemViewTest(TestCase):
    """カートアイテム更新ビューのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        
        self.customer = Customer.objects.create(
            username='update_user',
            age=28,
            email='update@example.com',
            sex='M'
        )
        
        self.product = Product.objects.create(
            name='更新テスト商品',
            price=Decimal('2000.00')
        )
        
        self.cart = Cart.objects.create(customer=self.customer)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )
        
        # セッションに顧客IDを設定
        session = self.client.session
        session['customer_id'] = self.customer.id
        session.save()
    
    def test_update_cart_item_quantity(self):
        """カートアイテムの数量が更新されることをテスト"""
        url = reverse('update_cart_item', args=[self.cart_item.id])
        response = self.client.post(url, {'quantity': 5})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # 数量が更新されたことを確認
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 5)
    
    def test_update_cart_item_returns_subtotal(self):
        """レスポンスに小計が含まれることをテスト"""
        url = reverse('update_cart_item', args=[self.cart_item.id])
        response = self.client.post(url, {'quantity': 3})
        
        data = response.json()
        self.assertIn('subtotal', data)
        # 2000 * 3 = 6000
        self.assertEqual(data['subtotal'], 6000.0)
    
    def test_update_cart_item_invalid_quantity(self):
        """無効な数量でエラーになることをテスト"""
        url = reverse('update_cart_item', args=[self.cart_item.id])
        response = self.client.post(url, {'quantity': 0})
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
    
    def test_update_cart_item_without_customer_session(self):
        """顧客セッションがない場合はエラーになることをテスト"""
        self.client.session.flush()
        
        url = reverse('update_cart_item', args=[self.cart_item.id])
        response = self.client.post(url, {'quantity': 2})
        
        self.assertEqual(response.status_code, 400)


class RemoveFromCartViewTest(TestCase):
    """カートアイテム削除ビューのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        
        self.customer = Customer.objects.create(
            username='remove_user',
            age=32,
            email='remove@example.com',
            sex='F'
        )
        
        self.product = Product.objects.create(
            name='削除テスト商品',
            price=Decimal('3000.00')
        )
        
        self.cart = Cart.objects.create(customer=self.customer)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        
        # セッションに顧客IDを設定
        session = self.client.session
        session['customer_id'] = self.customer.id
        session.save()
    
    def test_remove_from_cart(self):
        """カートアイテムが削除されることをテスト"""
        item_id = self.cart_item.id
        url = reverse('remove_from_cart', args=[item_id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # カートアイテムが削除されたことを確認
        self.assertFalse(CartItem.objects.filter(id=item_id).exists())
    
    def test_remove_from_cart_returns_cart_total(self):
        """レスポンスにカート合計が含まれることをテスト"""
        url = reverse('remove_from_cart', args=[self.cart_item.id])
        response = self.client.post(url)
        
        data = response.json()
        self.assertIn('cart_total', data)
        self.assertIn('cart_count', data)
    
    def test_remove_from_cart_without_customer_session(self):
        """顧客セッションがない場合はエラーになることをテスト"""
        self.client.session.flush()
        
        url = reverse('remove_from_cart', args=[self.cart_item.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 400)


class CartDetailViewTest(TestCase):
    """カート詳細ビューのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        
        self.customer = Customer.objects.create(
            username='detail_user',
            age=27,
            email='detail@example.com',
            sex='O'
        )
        
        self.product1 = Product.objects.create(name='商品1', price=Decimal('1000.00'))
        self.product2 = Product.objects.create(name='商品2', price=Decimal('2000.00'))
        
        self.cart = Cart.objects.create(customer=self.customer)
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)
        
        # セッションに顧客IDを設定
        session = self.client.session
        session['customer_id'] = self.customer.id
        session.save()
    
    def test_cart_detail_view_status_code(self):
        """カート詳細ページが正しく表示されることをテスト"""
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
    
    def test_cart_detail_view_template(self):
        """正しいテンプレートが使用されることをテスト"""
        response = self.client.get(reverse('cart_detail'))
        self.assertTemplateUsed(response, 'store/cart_detail.html')
    
    def test_cart_detail_view_context(self):
        """カートデータがコンテキストに含まれることをテスト"""
        response = self.client.get(reverse('cart_detail'))
        
        self.assertIn('cart', response.context)
        self.assertIn('cart_items', response.context)
        self.assertIn('total_price', response.context)
        self.assertIn('total_quantity', response.context)
        
        # データの確認
        self.assertEqual(len(response.context['cart_items']), 2)
        self.assertEqual(response.context['total_quantity'], 3)
        self.assertEqual(response.context['total_price'], Decimal('4000.00'))
    
    def test_cart_detail_without_customer_session(self):
        """顧客セッションがない場合でもページが表示されることをテスト"""
        self.client.session.flush()
        
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        
        # 空のカート情報が返されることを確認
        self.assertIsNone(response.context['cart'])
        self.assertEqual(len(response.context['cart_items']), 0)
        self.assertEqual(response.context['total_price'], 0)


class SetCustomerViewTest(TestCase):
    """顧客設定ビューのテスト（開発用）"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        
        self.customer = Customer.objects.create(
            username='session_user',
            age=24,
            email='session@example.com',
            sex='M'
        )
    
    def test_set_customer_in_session(self):
        """顧客IDがセッションに設定されることをテスト"""
        url = reverse('set_customer', args=[self.customer.id])
        response = self.client.get(url)
        
        # 商品一覧ページにリダイレクトされることを確認
        self.assertEqual(response.status_code, 302)
        
        # セッションに顧客IDが設定されたことを確認
        self.assertEqual(self.client.session.get('customer_id'), self.customer.id)
    
    def test_set_customer_invalid_id(self):
        """存在しない顧客IDの場合のテスト"""
        url = reverse('set_customer', args=[9999])
        response = self.client.get(url)
        
        # リダイレクトされることを確認
        self.assertEqual(response.status_code, 302)
        
        # セッションには設定されないことを確認
        self.assertIsNone(self.client.session.get('customer_id'))


if __name__ == '__main__':
    unittest.main()
