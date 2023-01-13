from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django_fac.core import payment as fac
from django_fac.core.entities import TransactionDetail, CardDetail, FACAuthorizationRedirectResponse
from .forms import PaymentForm
import uuid
import json

class PaymentView(View):
    def get(self, request):
        form = PaymentForm()
        return render(request, "fac_example/payment.html", { "form": form })

    def post(self, request):
        form = PaymentForm(request.POST)

        if form.is_valid():

            order_id = str(uuid.uuid1())
            amount = form.cleaned_data['amount']

            transaction = TransactionDetail(order_id, amount)
            redirect_url = self.get_redirect_url(request, order_id)
            card_detail = CardDetail(
                form.cleaned_data['card_number'], form.cleaned_data['card_cvv'], 
                form.cleaned_data['exp_date'], form.cleaned_data['card_holder_name']) 

            try:
                auth_response = fac.authorize(transaction, card_detail, redirect_url)
            except ValueError as ex:
                print(f"authorzed failed: {ex}")

            if auth_response.redirect_data:
                return HttpResponse(auth_response.redirect_data, content_type="text/html")
            else: 
                return HttpResponse(f"Invalid status code: {auth_response.status_code} :: Approved: {auth_response.approved}")

        return render(request, "fac_example/payment.html", { 
            'form': form, 
            'error': form.errors 
        })


    def get_redirect_url(self, request, order_id):
        redirect_path = reverse('webhook', kwargs={ 'order_id': order_id })
        return self.get_absolute_url(request, redirect_path)

    def get_absolute_url(self, request, url, force_https=False):
        current_site = get_current_site(request)
        domain = current_site.domain

        protocol = 'http'
        if request.is_secure() or force_https: 
            protocol = protocol + 's'

        return f'{protocol}://{domain}{url}'


@method_decorator(csrf_exempt, name='dispatch')
class FACResponseView(View):

    def post(self, request, order_id=None):
        fac_auth_response = FACAuthorizationRedirectResponse.from_response(request.POST)
        auth_response = fac_auth_response.response

        if auth_response.is_successful:
            payment_response = fac.payment(auth_response.spi_token)
            
            if payment_response.approved:
                trans_detail = TransactionDetail(payment_response.order_identifier, payment_response.total_amount)
                capture_response = fac.capture(trans_detail)

                if capture_response.approved:
                    return redirect("success")
                else:
                    return HttpResponse("Failed")

        return HttpResponse("Ok")


class SuccessView(View):
    def get(self, request):
        return render(request, "fac_example/success.html")
