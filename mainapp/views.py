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
class all_tg_user_langs(views.APIView):
    def get(self, request):
        user_lang_auth_objects = UserLangAuth.objects.all()
        user_lang_data = {}
        for obj in user_lang_auth_objects:
            user_lang_data[obj.tg_user_id] = obj.lang_code
        return Response(user_lang_data)
class all_tg_user_auth(views.APIView):
    def get(self, request):
        tg_user_ids = UserLangAuth.objects.filter(is_auth=True).values_list('tg_user_id', flat=True)
        tg_user_ids_list = list(tg_user_ids)
        return Response(tg_user_ids_list)

class CreateTgUser(views.APIView):
    def post(self, request):
        serializer = UserLangAuthCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeLangAPIView(views.APIView):
    def post(self, request):
        data = request.data
        tg_user = UserLangAuth.objects.get(tg_user_id=data['tg_user_id'])
        tg_user.lang_code = data['lang_code']
        tg_user.save()
        return Response(tg_user.lang_code, status=status.HTTP_200_OK)

class AuthenticateTgUser(views.APIView):
    def get(self, request, tg_user_id, user_id):
        user = UserLangAuth.objects.get(tg_user_id=tg_user_id)
        user.is_auth = True
        user.user = User.objects.get(pk=user_id)
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
        tg_user_id = str(creds.get('tg_user_id'))
        user = User.objects.get(email=email)
        if password == user.password:
            userAuth = UserLangAuth.objects.get(tg_user_id=tg_user_id)
            userAuth.user = user
            userAuth.is_auth = True
            userAuth.save()
            return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_400_BAD_REQUEST)

class GetUserAPIView(views.APIView):
    def get(self, request, tg_user_id):
        tg_user = UserLangAuth.objects.get(tg_user_id=tg_user_id)
        user = get_object_or_404(User, id=tg_user.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetUserPkAPIView(views.APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
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

################################ PAYMENT ###########################

class PaymentCreateAPIView(views.APIView):
    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Payment.objects.get(id=serializer.data.get('id'))
            card = Cards.objects.get(number=data.card_id)
            response = {
                "payment": PaymentSerializer(data).data,
                "card": CardsSerializer(card).data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetailAPIView(views.APIView):
    def get(self, request, pk):
        payment = Payment.objects.get(id=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PaymentAcceptAPIView(views.APIView):
    def get(self, request, pk):
        with transaction.atomic():
            payment = get_object_or_404(Payment, id=pk)
            user = get_object_or_404(User, id=payment.user.id)
            user.balance += payment.price
            payment.is_accepted = True
            payment.is_rejected = False
            user.save()
            payment.save()
        user_serializer = UserSerializer(user)
        payment_serializer = PaymentSerializer(payment)
        response = {
            "tg_user_id": get_object_or_404(UserLangAuth, user=user.id).tg_user_id,
            'user': user_serializer.data,
            'payment': payment_serializer.data}
        return Response(response, status=status.HTTP_200_OK)

class PaymentDeclineAPIView(views.APIView):
    def patch(self, request, pk):
        payment = get_object_or_404(Payment, id=pk)
        serializer = PaymentSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        user_serializer = UserSerializer(User.objects.get(id=payment.user.id))
        response = {
            "tg_user_id": get_object_or_404(UserLangAuth, user=user_serializer.data.get('id')).tg_user_id,
            'payment': serializer.data}
        return Response(response, status=status.HTTP_200_OK)

class PaymentListAPIView(views.APIView):
    def get(self, request):
        filter_by = request.query_params.get('filter_by')
        owner_by = request.query_params.get('owner_by')
        if filter_by:
            payments = self.filter_payments(filter_by)
        elif owner_by:
            user = get_object_or_404(UserLangAuth, tg_user_id=owner_by)
            payments = Payment.objects.filter(user=user.user).order_by("-datetime")
        else:
            payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def filter_payments(self, filter_by):
        if filter_by == 'requests':
            return Payment.objects.filter(is_accepted=False, is_rejected=False).order_by("-datetime")
        elif filter_by == 'done':
            return Payment.objects.filter(is_accepted=True, is_rejected=False).order_by("-datetime")
        elif filter_by == 'rejected':
            return Payment.objects.filter(is_accepted=False, is_rejected=True).order_by("-datetime")
        else:
            return Payment.objects.filter(is_accepted=False).order_by("-datetime")

################### ORDER #######################
class OrderCreateAPIView(views.APIView):
    def post(self, request):
        serializer = OrderDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListAPIView(views.APIView):
    def get(self, request):
        filter_by = request.query_params.get('filter_by')
        owner_by = request.query_params.get('owner_by')
        if filter_by:
            orders = self.filter_orders(filter_by)
        elif owner_by:
            user = get_object_or_404(UserLangAuth, tg_user_id=owner_by)
            orders = Order.objects.filter(user=user.user).order_by("-datetime")
        else:
            orders = Order.objects.all().order_by("-datetime")

        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_orders(self, filter_by):
        if filter_by == 'requests':
            return Order.objects.filter(is_completed=False, is_rejected=False).order_by("-datetime")
        elif filter_by == 'done':
            return Order.objects.filter(is_completed=True, is_rejected=False).order_by("-datetime")
        elif filter_by == 'rejected':
            return Order.objects.filter(is_completed=False, is_rejected=True).order_by("-datetime")
        else:
            return Order.objects.filter(is_completed=False).order_by("-datetime")

class OrderCompleteAPIView(views.APIView):
    def get(self, request, pk):
        with transaction.atomic():
            order = get_object_or_404(Order, id=pk)
            order.is_completed = True
            order.is_rejected = False

            user = get_object_or_404(User, id=order.user.id)
            user.balance -= order.product.price

            order.save()
            user.save()
        response_data = {
            "order": OrderDetailSerializer(order).data,
            "user": UserSerializer(user).data,
            "tg_user_id": get_object_or_404(UserLangAuth, user=user.id).tg_user_id
        }
        return Response(response_data, status=status.HTTP_200_OK)


class OrderRejectAPIView(views.APIView):
    def patch(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        serializer = OrderDetailSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        user_serializer = UserSerializer(User.objects.get(id=order.user.id))
        response = {
            "tg_user_id": get_object_or_404(UserLangAuth, user=user_serializer.data.get('id')).tg_user_id,
            'order': serializer.data}
        return Response(response, status=status.HTTP_200_OK)

class OrderDetailAPIView(views.APIView):
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CardsModelViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializer
    queryset = Cards.objects.all()

