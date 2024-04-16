from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mainapp.views import *

router = DefaultRouter()
router.register(r'cards', CardsModelViewSet, basename='cards')
router.register(r'app', AppsModelViewSet, basename='apps')
router.register(r'product', ProductsModelViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('user/get_tg_user/<int:pk>', check_user.as_view()),
    path('user/get_user/<int:tg_user_id>', GetUserAPIView.as_view()),
    path('user/createTgUser/', CreateTgUser.as_view()),
    path('user/createUser/', CreateUser.as_view()),
    path('user/authenticate/<int:pk>', AuthenticateTgUser.as_view()),
    path('user/is_authenticated/<int:pk>', CheckAuthentication.as_view()),
    path('user/deauthenticate/<int:pk>', DeauthenticateTgUser.as_view()),
    path('user/checkEmail/', CheckEmail.as_view()),
    path('user/checkPassword/', CheckPassword.as_view()),
    path('products/<int:app>', ProductsAppAPIView.as_view()),
    path('payment/create/<int:pk>', PaymentCreateAPIView.as_view()),
    path('payment/accept/<int:pk>', PaymentAcceptAPIView.as_view()),
    path('payment/reject/<int:pk>', PaymentDeclineAPIView.as_view()),
    path('payment/history/<int:user_id>', PaymentHistoryAPIView.as_view()),
    path('order/create/', OrderCreateAPIView.as_view()),
    path('order/requests/', OrderRequestsAPIView.as_view()),
    path('order/complete/<int:pk>', OrderCompleteAPIView.as_view()),
    path('order/history/<int:user_id>', OrderHistoryAPIView.as_view()),
]
