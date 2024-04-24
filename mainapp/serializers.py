from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserLangAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLangAuth
        fields = ['tg_user_id', 'lang_code', 'is_auth', 'user_id']
class UserLangAuthCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLangAuth
        fields = ['tg_user_id', 'lang_code', 'is_auth']

class CardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'

class AppDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    app = AppDetailSerializer()
    class Meta:
        model = Product
        fields = ['app', 'id', 'name', 'quantity', 'price']

    def get_app_info(self, obj):
        app = App.objects.filter(quiz_id=obj.id)
        serializer = AppDetailSerializer(app)
        return serializer.data

class ProductAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'price', 'cheque_pic', 'card_id', 'user']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

