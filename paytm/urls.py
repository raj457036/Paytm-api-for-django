from django.urls import path

from .views import (PaytmRequest, PaytmResponse, 
                    paytm_transection_status, TestPaytm) #,paytm_refund_request

app_name = 'paytm'

urlpatterns = [
    path('',PaytmRequest.as_view()),
    path('test/', TestPaytm.as_view()),
    path('payment_response/', PaytmResponse.as_view()),
    path('status/', paytm_transection_status),
    # path('refund_request/', paytm_refund_request)
]