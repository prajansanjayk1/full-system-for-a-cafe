from django.urls import path

from apps.payments import views

urlpatterns = [
    path("razorpay/orders/", views.create_payment_order_view, name="razorpay-order-create"),
    path("razorpay/verify/", views.verify_checkout_view, name="razorpay-checkout-verify"),
    path("razorpay/webhook/", views.razorpay_webhook_view, name="razorpay-webhook"),
]
