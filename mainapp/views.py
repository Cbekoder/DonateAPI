from django.apps.registry import Apps
from django.shortcuts import get_object_or_404
from rest_framework import views, status, viewsets
from rest_framework.response import Response
from django.db import transaction
from .serializers import *
from .models import *

class check_user(views.APIView):
    def get(self, request, pk):
        user = get_object_or_404(UserLangAuth, tg_user_id=pk)
        return Response(UserLangAuthSerializer(user).data, status=status.HTTP_200_OK)
class CreateTgUser(views.APIView):
    def post(self, request):
        serializer = UserLangAuthCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthenticateTgUser(views.APIView):
    def get(self, request, pk):
        user = UserLangAuth.objects.get(tg_user_id=pk)
        user.is_auth = True
        user.save()
        return Response("Success!", status=status.HTTP_200_OK)

class CheckAuthentication(views.APIView):
    def get(self, request, pk):
        user = UserLangAuth.objects.filter(tg_user_id=pk)[0]
        if user.is_auth == True:
            return Response(True, status=status.HTTP_200_OK)
        else:
            return Response(False, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_400_BAD_REQUEST)
class DeauthenticateTgUser(views.APIView):
    def get(self, request, pk):
        user = get_object_or_404(UserLangAuth, tg_user_id=pk)
        user.is_auth = False
        user.save()
        return Response(user.is_auth, status=status.HTTP_200_OK)


class CreateUser(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckEmail(views.APIView):
    def get(self, request):
        user = get_object_or_404(User, email=request.get_query_params('email'))
        return Response(user.email, status=status.HTTP_200_OK)

class CheckPassword(views.APIView):
    def get(self, request):
        creds = request.data
        email = creds.get('email')
        password = creds.get('password')
        user = User.objects.get(email=email)
        if password == user.password:
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_400_BAD_REQUEST)

class GetUserAPIView(views.APIView):
    def get(self, request, tg_user_id):
        user = get_object_or_404(User, user_id=tg_user_id)[0]
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppsModelViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppDetailSerializer

class ProductsModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductAllSerializer

class ProductsAppAPIView(views.APIView):
    def get(self, request, app):
        product = Product.objects.filter(app=app).order_by('price')
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PaymentCreateAPIView(views.APIView):
    def post(self, request, pk):
        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = User.objects.get(user_id=pk)
            serializer.save()
            data = Payment.objects.get(id=serializer.data['id'])
            resSerializer = PaymentListSerializer(data)
            return Response(resSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentRequestsAPIView(views.APIView):
    def get(self, request):
        payments = Payment.objects.filter(is_accepted=False, is_rejected=False).order_by("-datetime")
        serializer = PaymentListSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PaymentAcceptAPIView(views.APIView):
    def get(self, request, pk):
        with transaction.atomic():
            payment = get_object_or_404(Payment, id=pk)
            user = get_object_or_404(User, id=payment.user.id)
            user.balance += payment.price
            payment.is_accepted = True
            user.save()
            payment.save()
        user_serializer = UserSerializer(user)
        payment_serializer = PaymentListSerializer(payment)
        response = {
            'user': user_serializer.data,
            'payment': payment_serializer.data}
        return Response(response, status=status.HTTP_200_OK)

class PaymentDeclineAPIView(views.APIView):
    def get(self, request, pk):
        payments = get_object_or_404(Payment, id=pk)
        payments.is_rejected = True
        payments.save()
        return Response(payments.data, status=status.HTTP_200_OK)

class PaymentHistoryAPIView(views.APIView):
    def get(self, request, user_id):
        payments = Payment.objects.filter(user__user_id = user_id).order_by("-datetime")
        serializer = PaymentListSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderCreateAPIView(views.APIView):
    def post(self, request):
        serializer = OrderDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderRequestsAPIView(views.APIView):
    def get(self, request):
        orders = Order.objects.filter(is_completed=False).order_by("-datetime")
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderCompleteAPIView(views.APIView):
    def get(self, request, pk):
        with transaction.atomic():
            order = get_object_or_404(Order, id=pk)
            order.is_completed = True

            user = get_object_or_404(User, id=order.user.id)
            user.balance -= order.product.price

            order.save()
            user.save()
        response_data = {
            "order": OrderDetailSerializer(order).data,
            "user": UserSerializer(user).data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class OrderHistoryAPIView(views.APIView):
    def get(self, request, user_id):
        orders = Order.objects.filter(user__user_id=user_id).order_by("-datetime")
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CardsModelViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    queryset = Cards.objects.all()

