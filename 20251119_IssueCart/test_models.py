"""
カート機能のユニットテスト

Issue: カートに入れる機能実装
日付: 2025-11-19

このテストファイルでは以下をテストします：
1. Customerモデルの作成とバリデーション
2. Cartモデルの作成とCustomerとの関連
3. CartItemモデルの作成と商品追加
4. カート内の商品数量計算
5. カート内の合計金額計算
"""

import unittest
from decimal import Decimal
from django.test import TestCase
from store.models import Product, Customer, Cart, CartItem


class CustomerModelTest(TestCase):
    """Customerモデルのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.customer_data = {
            'username': 'test_user',
            'age': 25,
            'email': 'test@example.com',
            'sex': 'M'
        }
    
    def test_create_customer(self):
        """顧客の作成テスト"""
        customer = Customer.objects.create(**self.customer_data)
        self.assertEqual(customer.username, 'test_user')
        self.assertEqual(customer.age, 25)
        self.assertEqual(customer.email, 'test@example.com')
        self.assertEqual(customer.sex, 'M')
    
    def test_customer_str_representation(self):
        """顧客の文字列表現テスト"""
        customer = Customer.objects.create(**self.customer_data)
        expected = f"test_user (test@example.com)"
        self.assertEqual(str(customer), expected)
    
    def test_customer_email_unique(self):
        """顧客メールアドレスの一意性テスト"""
        Customer.objects.create(**self.customer_data)
        
        # 同じメールアドレスで別の顧客を作成しようとするとエラー
        with self.assertRaises(Exception):
            Customer.objects.create(
                username='another_user',
                age=30,
                email='test@example.com',  # 重複
                sex='F'
            )
    
    def test_customer_sex_choices(self):
        """顧客の性別選択肢テスト"""
        # 正しい選択肢
        for sex in ['M', 'F', 'O']:
            customer = Customer.objects.create(
                username=f'user_{sex}',
                age=25,
                email=f'{sex}@example.com',
                sex=sex
            )
            self.assertEqual(customer.sex, sex)


class CartModelTest(TestCase):
    """Cartモデルのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.customer = Customer.objects.create(
            username='cart_user',
            age=30,
            email='cart@example.com',
            sex='F'
        )
        
        self.product1 = Product.objects.create(
            name='商品A',
            price=Decimal('1000.00')
        )
        
        self.product2 = Product.objects.create(
            name='商品B',
            price=Decimal('2000.00')
        )
    
    def test_create_cart(self):
        """カートの作成テスト"""
        cart = Cart.objects.create(customer=self.customer)
        self.assertEqual(cart.customer, self.customer)
        self.assertIsNotNone(cart.created_at)
        self.assertIsNotNone(cart.updated_at)
    
    def test_cart_str_representation(self):
        """カートの文字列表現テスト"""
        cart = Cart.objects.create(customer=self.customer)
        expected = f"cart_userのカート (ID: {cart.id})"
        self.assertEqual(str(cart), expected)
    
    def test_cart_total_price_empty(self):
        """空のカートの合計金額テスト"""
        cart = Cart.objects.create(customer=self.customer)
        self.assertEqual(cart.get_total_price(), 0)
    
    def test_cart_total_price_with_items(self):
        """商品が入ったカートの合計金額テスト"""
        cart = Cart.objects.create(customer=self.customer)
        
        # 商品Aを2個追加
        CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        # 商品Bを1個追加
        CartItem.objects.create(cart=cart, product=self.product2, quantity=1)
        
        # 合計: 1000 * 2 + 2000 * 1 = 4000
        expected_total = Decimal('4000.00')
        self.assertEqual(cart.get_total_price(), expected_total)
    
    def test_cart_total_quantity_empty(self):
        """空のカートの商品総数テスト"""
        cart = Cart.objects.create(customer=self.customer)
        self.assertEqual(cart.get_total_quantity(), 0)
    
    def test_cart_total_quantity_with_items(self):
        """商品が入ったカートの商品総数テスト"""
        cart = Cart.objects.create(customer=self.customer)
        
        CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=cart, product=self.product2, quantity=3)
        
        # 合計: 2 + 3 = 5
        self.assertEqual(cart.get_total_quantity(), 5)
    
    def test_multiple_carts_per_customer(self):
        """1顧客が複数のカートを持てることをテスト"""
        cart1 = Cart.objects.create(customer=self.customer)
        cart2 = Cart.objects.create(customer=self.customer)
        
        customer_carts = Cart.objects.filter(customer=self.customer)
        self.assertEqual(customer_carts.count(), 2)


class CartItemModelTest(TestCase):
    """CartItemモデルのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.customer = Customer.objects.create(
            username='item_user',
            age=28,
            email='item@example.com',
            sex='M'
        )
        
        self.cart = Cart.objects.create(customer=self.customer)
        
        self.product = Product.objects.create(
            name='テスト商品',
            price=Decimal('1500.00')
        )
    
    def test_create_cart_item(self):
        """カートアイテムの作成テスト"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )
        
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 1)
        self.assertIsNotNone(cart_item.added_at)
    
    def test_cart_item_str_representation(self):
        """カートアイテムの文字列表現テスト"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=3
        )
        expected = f"テスト商品 x 3"
        self.assertEqual(str(cart_item), expected)
    
    def test_cart_item_subtotal(self):
        """カートアイテムの小計計算テスト"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=5
        )
        
        # 小計: 1500 * 5 = 7500
        expected_subtotal = Decimal('7500.00')
        self.assertEqual(cart_item.get_subtotal(), expected_subtotal)
    
    def test_cart_item_unique_together(self):
        """カートと商品の組み合わせが一意であることをテスト"""
        # 最初のアイテムを作成
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )
        
        # 同じカートと商品の組み合わせで作成しようとするとエラー
        with self.assertRaises(Exception):
            CartItem.objects.create(
                cart=self.cart,
                product=self.product,
                quantity=2
            )
    
    def test_cart_item_default_quantity(self):
        """カートアイテムのデフォルト数量テスト"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product
            # quantityを指定しない
        )
        
        # デフォルト値は1
        self.assertEqual(cart_item.quantity, 1)
    
    def test_cart_item_update_quantity(self):
        """カートアイテムの数量更新テスト"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )
        
        # 数量を更新
        cart_item.quantity = 10
        cart_item.save()
        
        # データベースから再取得して確認
        updated_item = CartItem.objects.get(id=cart_item.id)
        self.assertEqual(updated_item.quantity, 10)
    
    def test_cart_item_deletion(self):
        """カートアイテムの削除テスト"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )
        
        item_id = cart_item.id
        cart_item.delete()
        
        # 削除されたことを確認
        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(id=item_id)


class CartIntegrationTest(TestCase):
    """カート機能の統合テスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.customer = Customer.objects.create(
            username='integration_user',
            age=35,
            email='integration@example.com',
            sex='O'
        )
        
        # 複数の商品を作成
        self.products = [
            Product.objects.create(name=f'商品{i}', price=Decimal(f'{(i+1)*1000}.00'))
            for i in range(5)
        ]
    
    def test_shopping_scenario(self):
        """実際の買い物シナリオをテスト"""
        # カートを作成
        cart = Cart.objects.create(customer=self.customer)
        
        # 商品を3つカートに追加
        CartItem.objects.create(cart=cart, product=self.products[0], quantity=2)
        CartItem.objects.create(cart=cart, product=self.products[1], quantity=1)
        CartItem.objects.create(cart=cart, product=self.products[2], quantity=3)
        
        # 商品総数を確認: 2 + 1 + 3 = 6
        self.assertEqual(cart.get_total_quantity(), 6)
        
        # 合計金額を確認: 1000*2 + 2000*1 + 3000*3 = 13000
        expected_total = Decimal('13000.00')
        self.assertEqual(cart.get_total_price(), expected_total)
        
        # カート内のアイテム数を確認
        self.assertEqual(cart.items.count(), 3)
    
    def test_update_cart_item_quantity(self):
        """カートアイテムの数量変更シナリオをテスト"""
        cart = Cart.objects.create(customer=self.customer)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.products[0],
            quantity=1
        )
        
        # 初期の合計
        initial_total = cart.get_total_price()
        self.assertEqual(initial_total, Decimal('1000.00'))
        
        # 数量を5に変更
        cart_item.quantity = 5
        cart_item.save()
        
        # 合計が更新されることを確認
        updated_total = cart.get_total_price()
        self.assertEqual(updated_total, Decimal('5000.00'))
    
    def test_remove_cart_item(self):
        """カートからアイテムを削除するシナリオをテスト"""
        cart = Cart.objects.create(customer=self.customer)
        
        item1 = CartItem.objects.create(cart=cart, product=self.products[0], quantity=2)
        item2 = CartItem.objects.create(cart=cart, product=self.products[1], quantity=3)
        
        # 初期状態の確認
        self.assertEqual(cart.items.count(), 2)
        self.assertEqual(cart.get_total_quantity(), 5)
        
        # 1つ目のアイテムを削除
        item1.delete()
        
        # 削除後の確認
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.get_total_quantity(), 3)
        self.assertEqual(cart.get_total_price(), Decimal('6000.00'))


if __name__ == '__main__':
    unittest.main()
