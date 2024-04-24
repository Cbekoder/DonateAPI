from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    balance = models.PositiveIntegerField()

    def __str__(self):
        return self.email

class UserLangAuth(models.Model):
    tg_user_id = models.CharField(max_length=15, primary_key=True)
    lang_code = models.CharField(max_length=5)
    is_auth = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)

    def __str__(self):
        return self.tg_user_id


class App(models.Model):
    name = models.CharField(max_length=50)
    app_pic = models.JSONField()

    def __str__(self):
        return self.name

class Product(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name + " " + str(self.quantity)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    gamer_id = models.CharField(max_length=50, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.name + " " + self.product.name

class Cards(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=16, unique=True)
    type = models.CharField(max_length=10,
                            choices=[
                                ('Humo', 'Humo'),
                                ('Uzcard', 'Uzcard'),
                                ('Visa', 'Visa')])
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.number

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cheque_pic = models.JSONField()
    card_id = models.ForeignKey(Cards, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.datetime) + ": " + self.user.name + " - " + str(self.price)
