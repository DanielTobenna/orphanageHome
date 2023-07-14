from django.shortcuts import render, redirect, reverse

from django.core.mail import BadHeaderError, send_mail

from django.http import HttpResponse,HttpResponseRedirect

from django.contrib import messages

from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.forms import UserCreationForm

from django.core.mail import EmailMessage

from django.conf import settings

from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives

from .models import *

#from .forms import *

from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required

from django.utils.html import strip_tags

import datetime
import json
import requests
import uuid
import os

# Create your views here.

def home(request):
	return render(request, 'orphanageHomeapp/index.html')

def about(request):
	return render(request, 'orphanageHomeapp/company.html')

def agriculture(request):
	return render(request, 'orphanageHomeapp/agriculture.html')

def contact(request):
	return HttpResponse('Get in touch with us using Support@yanahomes.in')

def career(request):
	return render(request, 'orphanageHomeapp/career.html')

def donate(request):
	if request.method=='POST':
		#post data to create invoice for payment
		client_email= request.Post.get('email')
		price_amount= request.POST.get('price_amount')
		price_currency= request.POST.get('price_currency')
		pay_currency= request.POST.get('pay_currency')
		order_id= 'Donation to Yana Homes'
		order_description= "This is a donation..."
		if price_amount and pay_currency:
			# Api's url link
			url= 'https://api.nowpayments.io/v1/invoice'
			payload=json.dumps({
				"price_amount": price_amount,
				"price_currency": price_currency,
				"pay_currency": pay_currency,
				"order_id": order_id,
				"order_description": order_description,
				"ipn_callback_url": "https://nowpayments.io",
				"success_url": "https://www.yanahomes.in",
				#our success url will direct us to the get_payment_status view for balance top ups
				"cancel_url": "https://www.yanahomes.in"
			})
			headers={'x-api-key':'', 'Content-Type': 'application/json'}
			response= requests.request('POST', url, headers=headers, data=payload)
			res= response.json()
			print(res)
			generated_link= res["invoice_url"]
			generated_payment_id= res["id"]
			#Now get the user and add the payment ID to the database as we will be using it to know their payment status
			template= render_to_string('orphanageHomeapp/pendingDepositEmail.html', {'name': client_email, 'amount':price_amount, 'transaction_id':generated_payment_id})
			plain_message= strip_tags(template)
			emailmessage= EmailMultiAlternatives(
				'Pending Deposit Order',
				plain_message,
				settings.EMAIL_HOST_USER,
				[client_email],
				)
			emailmessage.attach_alternative(template, 'text/html')
			emailmessage.send()
			try:
				send_mail(client_email, "A client with username: {} has created a deposit request with an amount ${}".format(client_email, price_amount),settings.EMAIL_HOST_USER, ['info@yanahomes.in'])
			except BadHeaderError:
				pass
			return redirect(generated_link)
	return render(request, 'orphanageHomeapp/deposit.html')

def healthcare(request):
	return render(request, 'orphanageHomeapp/healthcare.html')

def privacy(request):
	return render(request, 'orphanageHomeapp/privacy.html')

def skillshop(request):
	return render(request, 'orphanageHomeapp/skillshop.html')

def terms(request):
	return render(request, 'orphanageHomeapp/terms.html')

def otherpayment(request):
	return HttpResponse('This payment is not available through our website at the moment. Please contact our support team using support@yanahomes.in')
