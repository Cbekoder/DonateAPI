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
    path('user/all_user_lang/', all_tg_user_langs.as_view()),
    path('user/all_user_auth/', all_tg_user_auth.as_view()),
    path('user/get_user/<int:tg_user_id>', GetUserAPIView.as_view()),
    path('user/get_user_pk/<int:pk>', GetUserPkAPIView.as_view()),
    path('user/createTgUser/', CreateTgUser.as_view()),
    path('user/changeLang/', ChangeLangAPIView.as_view()),
    path('user/createUser/', CreateUser.as_view()),
    path('user/authenticate/<int:tg_user_id>/<int:user_id>', AuthenticateTgUser.as_view()),
    path('user/is_authenticated/<int:pk>', CheckAuthentication.as_view()),
    path('user/deauthenticate/<int:pk>', DeauthenticateTgUser.as_view()),
    path('user/checkEmail/', CheckEmail.as_view()),
    path('user/checkPassword/', CheckPassword.as_view()),
    path('products/<int:app>', ProductsAppAPIView.as_view()),
    path('payment/create/', PaymentCreateAPIView.as_view()),
    path('payment/accept/<int:pk>', PaymentAcceptAPIView.as_view()),
    path('payment/reject/<int:pk>', PaymentDeclineAPIView.as_view()),
    path('payment/list/', PaymentListAPIView.as_view()),
    path('payment/detail/<int:pk>', PaymentDetailAPIView.as_view()),
    path('order/detail/<int:pk>', OrderDetailAPIView.as_view()),
    path('order/create/', OrderCreateAPIView.as_view()),
    path('order/list/', OrderListAPIView.as_view()),
    path('order/complete/<int:pk>', OrderCompleteAPIView.as_view()),
    path('order/reject/<int:pk>', OrderRejectAPIView.as_view()),
]