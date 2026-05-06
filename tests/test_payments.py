import hmac
from hashlib import sha256

import pytest
from django.test import override_settings

from apps.payments.services import PaymentSignatureError, verify_checkout_signature


@override_settings(RAZORPAY_KEY_SECRET="secret")
def test_checkout_signature_verification():
    signature = hmac.new(b"secret", b"order_1|pay_1", sha256).hexdigest()
    verify_checkout_signature(provider_order_id="order_1", provider_payment_id="pay_1", signature=signature)


@override_settings(RAZORPAY_KEY_SECRET="secret")
def test_checkout_signature_rejects_tampering():
    with pytest.raises(PaymentSignatureError):
        verify_checkout_signature(provider_order_id="order_1", provider_payment_id="pay_1", signature="bad")
