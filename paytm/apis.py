from .utils import *
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import settings

paytm_sets = settings.PAYTM_GATEWAY_SETTINGS

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class PaytmRequest(TemplateView):
    template_name = 'request.html'


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['paytm_payment_data'] = {}
        for key, value in paytm_sets.items():
            ctx['paytm_payment_data'].update({key:value})
        
        for key in ('ORDER_ID', 'TXN_AMOUNT', 'CUST_ID'):
            ctx['paytm_payment_data'].update({key:self.request.POST.get(key)})
        ctx['paytm_payment_data'].update({
                'CHECKSUMHASH':generate_checksum(ctx['paytm_payment_data'], settings.PAYTM_MERCHANT_KEY)
            })

        ctx['payment_url'] = settings.PAYTM_STAGING_URL+
        return ctx

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class PaytmResponse(TemplateView):

    template_name = 'response.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['response_data'] = {}
        for key, value in self.request.POST.items():
            ctx['response_data'].update({key:value})
        ctx['response_data'].update({
            'verified':verify_checksum(ctx['response_data'], settings.PAYTM_MERCHANT_KEY, ctx['response_data']['CHECKSUMHASH'])
            })
        return ctx

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

