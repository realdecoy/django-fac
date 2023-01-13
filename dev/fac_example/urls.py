from django.urls import path
from .views import PaymentView, SuccessView, FACResponseView

urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
    path('success/', SuccessView.as_view(), name='success'),

    path('webhook/', FACResponseView.as_view(), name='webhook'),
    path('webhook/<str:order_id>', FACResponseView.as_view(), name='webhook'),
]
