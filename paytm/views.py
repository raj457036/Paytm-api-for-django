from .utils import generate_checksum, verify_checksum, generate_refund_checksum
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import settings
from django.forms import ValidationError
from json import dumps
from urllib import request as rq, parse

from .models import PaytmDataBase #,PaytmRefundDataBase

paytm_sets = settings.PAYTM_GATEWAY_SETTINGS
txn_status_url = '/merchant-status/getTxnStatus'
txn_request_url = '/theia/processTransaction'

# prefer dash board for refunds
rfnd_request_url = '/refund/HANDLER_INTERNAL/REFUND'
rfnd_status_url = '/refund/HANDLER_INTERNAL/getRefundStatus'

class TestPaytm(TemplateView):
    template_name = 'paytm/test.html'


@method_decorator(csrf_exempt, name='dispatch')
class PaytmRequest(LoginRequiredMixin, TemplateView):
    template_name = 'paytm/request.html'

    def get_payment_data(self):
        req_data = {}

        if self.request.POST.get('PAYMENT_MODE_ONLY') == 'Yes':
            if not all(key in self.request.POST for key in ('AUTH_MODE', 'PAYMENT_TYPE_ID', 'CARD_TYPE', 'BANK_CODE')):
                raise ValidationError("please provide all these fields too: ('AUTH_MODE', 'PAYMENT_TYPE_ID', 'CARD_TYPE', 'BANK_CODE')")

        req_data.update(dict(map(lambda key:key, paytm_sets.items())))

        req_data.update(dict(map(lambda key:key, self.request.POST.items())))
        req_data.pop('csrfmiddlewaretoken')

        return req_data


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['paytm_req_data'] = self.get_payment_data()

        ctx['paytm_req_data'].update({
                'CHECKSUMHASH':generate_checksum(ctx['paytm_req_data'], settings.PAYTM_MERCHANT_KEY)
            })

        ctx['paytm_url'] = settings.PAYTM_URL+txn_request_url
        return ctx

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



@method_decorator(csrf_exempt, name='dispatch')
class PaytmResponse(TemplateView):

    template_name = 'paytm/response.html'

    def save_transection(self, response_data):
        PaytmDataBase.objects.update_or_create(order_id=response_data.get('ORDERID'), 
                                amount=response_data.get('TXNAMOUNT'),
                                checksumhash=response_data.get('CHECKSUMHASH'),
                                txn_id=response_data.get('TXNID'))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        response_data = {}
        for key, value in self.request.POST.items():
            response_data.update({key:value})

        if settings.PAYTM_SAVE_SUCCESS_TRANSECTIONS_ONLY:
            if response_data.get('RESPCODE') == '01':
                self.save_transection(response_data)
        else:
            self.save_transection(response_data)

        verified = verify_checksum(response_data, settings.PAYTM_MERCHANT_KEY, response_data['CHECKSUMHASH'])
        response_data.update({'checksum verified': verified })

        ctx['response_data'] = dumps(response_data)
        return ctx

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@login_required
def paytm_transection_status(request):
    if request.method == 'POST':
        order = get_object_or_404(PaytmDataBase, order_id=request.POST.get('ORDER_ID'))
        data = {}
        data.update({
            'MID':paytm_sets['MID'],
            'CHECKSUMHASH':order.checksumhash,
            'ORDERID':order.order_id })

        data = parse.urlencode({'JsonData':data}).encode()
        req =  rq.Request(settings.PAYTM_URL+txn_status_url, data=data)
        return JsonResponse((rq.urlopen(req)).read().decode('utf-8'), safe=False)
    return JsonResponse('only post method allowed!', safe=False)


# def paytm_refund_request(request):
#     if request.method == 'POST':
#         order = get_object_or_404(PaytmDataBase, order_id=request.POST.get('ORDER_ID'))
#         refund_o = PaytmRefundDataBase.objects.get_or_create(order_id=order.id)[0]
#         amount = request.POST.get('AMOUNT', order.amount)

#         if amount == '' or float(amount) > order.amount:
#             amount = order.amount

#         data = {
#             'MID': paytm_sets['MID'],
#             'REFID':  str(refund_o.id),
#             'TXNID': str(order.txn_id),
#             'ORDERID': str(order.id),
#             'REFUNDAMOUNT': str(amount),
#             'COMMENTS':request.POST.get('COMMENT', 'Refund complete.')
#         }
#         checksumhash = generate_refund_checksum(data, settings.PAYTM_MERCHANT_KEY)
#         data.update({
#             'TXNTYPE':'REFUND',
#             'CHECKSUM':checksumhash })
#         refund_o.checksumhash = checksumhash
#         refund_o.save()

#         data = parse.urlencode({'JsonData':data}).encode('utf-8')
#         req =  rq.Request(settings.PAYTM_URL+rfnd_request_url, data=data)
#         return HttpResponse((rq.urlopen(req)).read().decode('utf-8'))
#     return JsonResponse('only post method allowed!', safe=False)
        