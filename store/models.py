from django.db import models


class Product(models.Model):
    """商品モデル"""
    name = models.CharField(max_length=100, verbose_name="商品名")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="価格")

    class Meta:
        ordering = ["id"]
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return f"{self.name} (¥{self.price})"


class Customer(models.Model):
    """顧客モデル - age, email, sexプロパティを持つ"""
    SEX_CHOICES = [
        ('M', '男性'),
        ('F', '女性'),
        ('O', 'その他'),
    ]
    
    username = models.CharField(max_length=100, unique=True, verbose_name="ユーザー名")
    age = models.IntegerField(verbose_name="年齢")
    email = models.EmailField(unique=True, verbose_name="メールアドレス")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name="性別")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    
    class Meta:
        ordering = ["id"]
        verbose_name = "顧客"
        verbose_name_plural = "顧客"
    
    def __str__(self):
        return f"{self.username} ({self.email})"


class Cart(models.Model):
    """カートモデル - Customer単位で管理"""
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='carts',
        verbose_name="顧客"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "カート"
        verbose_name_plural = "カート"
    
    def __str__(self):
        return f"{self.customer.username}のカート (ID: {self.id})"
    
    def get_total_price(self):
        """カート内の合計金額を計算"""
        return sum(item.get_subtotal() for item in self.items.all())
    
    def get_total_quantity(self):
        """カート内の商品総数を計算"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """カートアイテムモデル - CartとProductの中間テーブル"""
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="カート"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name="商品"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="追加日時")
    
    class Meta:
        ordering = ["id"]
        verbose_name = "カートアイテム"
        verbose_name_plural = "カートアイテム"
        # カートと商品の組み合わせは一意にする
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_subtotal(self):
        """商品の小計を計算"""
        return self.product.price * self.quantity