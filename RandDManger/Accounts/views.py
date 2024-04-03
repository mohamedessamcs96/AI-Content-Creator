from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import HttpResponse
import datetime
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
import re
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404, handler500
from rest_framework import status
from PIL import Image
from io import BytesIO
import base64
from django.http import HttpResponse
from accept.payment import *
from django import forms
from .models import UserAdmin, HomeInfo,ProjectManger,ContentCreator
from .forms import AdminForm, LoginForm,HomeInfoForm,ContentCreatorForm
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .contentwriterbot import ContentWriterBot
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CardInformationSerializer
from django.views import View
import stripe
from django.views.generic import TemplateView
from .report_generator import CreateReportPdf




@login_required(login_url='/ar/login/')
def admin_panel(request):
    language_code = request.path.split('/')[1]  # Extract the first part of the path

    homeinfo = HomeInfo.objects.get(id=1)
    home_background = language_code + homeinfo.background.url
    template_name = 'admin_panel.html' if language_code == 'en' else 'admin_panel-ar.html'
    return render(request, template_name, {"language_code": language_code, 'home_background': home_background})


# Create an error message function
def get_error_message(request):
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    email = request.POST['email']
    username = request.POST.get('username')
    #Username = request.POST['Username']
    if password1 != password2:
        return "The Passwords didn't match"
    if UserAdmin.objects.filter(email=email).exists():
        return "Email already exists"
    # if UserAdmin.objects.filter(Username=Username).exists():
    #     return "Username should be unique!"

    # Check if the username or email already exists
    if UserAdmin.objects.filter(username=username).exists():
        return "Username should be unique!"





def signup(request):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    # load the home background
    homeinfo = HomeInfo.objects.get(id=1)
    home_background = language_code + homeinfo.background.url
    template_name = 'signup.html' if language_code == 'en' else 'signup-ar.html'
    
    if request.method == "POST":
        form = AdminForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request, "Register successful")
            return redirect(f'/{language_code}/')

        messages.error(request, get_error_message(request))
        return render(request, template_name, context={'register_form': form, "language_code": language_code,
                                                        'home_background': home_background})
    else:
        form = AdminForm()
        return render(request, template_name, context={'register_form': form, "language_code": language_code,
                                                        'home_background': home_background})






# Create your views here.

@login_required(login_url='/ar/login/')
def register_request(request):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    # load the home background
    homeinfo = HomeInfo.objects.get(id=1)
    home_background = language_code + homeinfo.background.url
    template_name = 'register.html' if language_code == 'en' else 'register-ar.html'
    if request.user.is_superuser or request.user.is_admin:
        if request.method == "POST":
            form = AdminForm(request.POST)
            if form.is_valid():
                user = form.save()

                messages.success(request, "Register successful")
                return redirect(f'/{language_code}/')

            messages.error(request, get_error_message(request))
            return render(request, template_name, context={'register_form': form, "language_code": language_code,
                                                           'home_background': home_background})
        else:
            form = AdminForm()
            return render(request, template_name, context={'register_form': form, "language_code": language_code,
                                                           'home_background': home_background})
    else:
        return render(request, 'notallowed.html',
                      context={"language_code": language_code, 'home_background': home_background})


def logout_request(request):
    logout(request)
    messages.info(request, "You have sucessfully logged out")
    return redirect("login")


# Create your views here.
def login_request(request):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    # load the home background
    homeinfo = HomeInfo.objects.get(id=1)
    home_background = language_code + homeinfo.background.url
    template_name = 'login.html' if language_code == 'en' else 'login-ar.html'

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            # username=form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # user=authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as {username}")
                return redirect(f'/{language_code}/')
            else:
                messages.error(request, "Invalid username and password!")
        else:
            messages.error(request, "Invalid form")

    form = LoginForm()
    return render(request, template_name,
                  context={'login_form': form, "language_code": language_code, 'home_background': home_background})


def logout_request(request):
    logout(request)
    messages.info(request, "You have sucessfully logged out")
    return redirect("login")

#@cache_page(60*15, cache="special_cache")
@login_required(login_url='/ar/login/')
def home_page(request):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    template_name = 'home.html' if language_code == 'en' else 'home-ar.html'


    homeinfo = HomeInfo.objects.get(id=1)

    home_background = str(homeinfo.background.url).lstrip('/')

    print(home_background)
    print(template_name)
    return render(request, template_name,
                  {"homeinfo": homeinfo, "language_code": language_code,
                   'home_background': home_background})


@login_required(login_url='/en/login/')
def content_creator(request):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    template_name = 'content_creator.html' if language_code == 'en' else 'content_creator-ar.html'

    
    form = ContentCreatorForm(request.POST)
    homeinfo = HomeInfo.objects.get(id=1)

    home_background = str(homeinfo.background.url).lstrip('/')

    if request.method == 'GET':
        form = ContentCreatorForm(request.POST)
        print("User is upgraded:",request.user.is_upgraded)
        if not request.user.is_upgraded:            
      
            today_date = datetime.now().date()

            # Calculate the date 7 days ago
            seven_days_ago = today_date - timedelta(days=7)
  
            print("last execution",request.user.last_execution_time.date())  
            print("7 days execution",seven_days_ago)  
            print(seven_days_ago >= request.user.last_execution_time.date())
            # Check if the last execution time is 7 days ago or more
            if  seven_days_ago >= request.user.last_execution_time.date():
                trial = True
                return render(request, template_name,
                {"homeinfo": homeinfo, "language_code": language_code,
                'home_background': home_background,'form':form,"trial":trial})  
            else:
                trial = False
                return render(request, template_name,
                {"homeinfo": homeinfo, "language_code": language_code,
                'home_background': home_background,'form':form,"trial":trial})  
        else:
            trial = True
            return render(request, template_name,
            {"homeinfo": homeinfo, "language_code": language_code,
            'home_background': home_background,'form':form,"trial":trial})     

    if request.method == 'POST':
            if form.is_valid():
                form.save()
                bot=ContentWriterBot()
                response,content_type=bot.resample_message(request)
                content = bot.generate_response(response)  # Generate the response
                try:
                    print(content.content.split('\n')[0])
                    img_prompt=content.content.split('\n')[0]
                    img=bot.generate_image(content.content.split('\n')[0])
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                except Exception as e:
                    print(e)

                print("Bot:")
                # img_str=None
                lines = content.content.split('\n')
                script= content.content
                print(lines)
                paragraph=[]

                title = re.sub(r'\*\*(.*?)\*\*', r'\1', lines[0])
                # Remove the title line from the list
                lines = lines[1:]
                
                table=bot.format_result(lines)
                print(len(table))

                for line in lines:
                    if line.strip():  # Check if the line is not empty
                        # Remove the bold reqular expressons
                        clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
                        paragraph.append(clean_text)


                print("paragraph",paragraph)
                #Generate image
                # img=bot.generate_image("title")
                usage_queryset = UserAdmin.objects.filter(username=request.user.username)
                usage_queryset.last_execution_time = datetime.now().date()
                # Check if any UserAdmin object matches the query
                if usage_queryset.exists():
                    # Get the first UserAdmin object from the queryset
                    usage = usage_queryset.first()
                    # Update the last_execution_time to the current date
                    usage.last_execution_time = datetime.now().date()
                    # Save the changes back to the database
                    usage.save() 

                if content_type=="Social Media POST Content":
                    title,paragraph=bot.format_social_post(script)
                    img=bot.generate_image(img_prompt)
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")
                    print(img)
                    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    print(img_str)
                elif content_type=="Video Content Script":
                    while(len(table)<=85):
                        lines = content.content.split('\n')
                        script= content.content
                        print(lines)
                        paragraph=[]
                        # Extract the title from the first line

                        title = re.sub(r'\*\*(.*?)\*\*', r'\1', lines[0])
                        # Remove the title line from the list
                        lines = lines[1:]                
                        content = bot.generate_response(response)  # Generate the response
                        table=bot.format_result(lines)
                        # data,table=bot.format_result(lines)

                else:
                    pass
                
                language_code = request.path.split('/')[1]  # Extract the first part of the path
                template_name = 'content.html' if language_code == 'en' else 'content-ar.html'
                
                #p = ProjectManger.objects.create(admin=request.user, task=task, results=bot)
                return render(request, template_name,{"language_code": language_code,"paragraph":paragraph,"title":title,"table":table,"img_str":img_str,"content_type":content_type,"script":script,'data':'data'})
            
                        

    

def create_report(request,data):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    report=CreateReportPdf()
    # lines=data.split('\n')
    # lines = [line.strip() for line in lines.split('!') + lines.split('?') + lines.split('.') +lines.split('-')]
    # # Remove empty lines
    # lines = [line for line in lines if line]
    # title=lines[0]
    # paragraph=lines[1:]
    story=report.generate_report(data)
    return story


@login_required(login_url='/ar/login/')
def home_info(request):
    """Process images uploaded by users"""
    form = HomeInfoForm()
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    # load the home background
    homeinfo = HomeInfo.objects.get(id=1)
    home_background = language_code + homeinfo.background.url
    homeinfotable = HomeInfo.objects.get(pk=1)  # Assuming you have only one instance
    print(homeinfotable)
    # Create an instance of the form with initial values
    form = HomeInfoForm(initial={
        'title': homeinfotable.title,
        'title_ar_field': homeinfotable.title_ar_field,
        'image': homeinfotable.image.url if homeinfotable.image else '',
        'description_ar_field': homeinfotable.description_ar_field,
    })
    if request.method == 'POST':
        # Update the values of AnalysisPrices object
        homeinfotable.title = request.POST['title']
        homeinfotable.title_ar_field = request.POST['title_ar_field']
        homeinfotable.image = request.FILES['image']
        homeinfotable.description = request.POST['description']
        homeinfotable.description_ar_field = request.POST['description_ar_field']

        homeinfotable.save()
        return redirect(f'/{language_code}/')


    else:
        form = HomeInfoForm()
        return render(request, 'add_home_info.html',
                      {'form': form, "language_code": language_code, 'home_background': home_background})


# Master Cards :link https://docs.stripe.com/testing#cards


@login_required(login_url='login')
def product_page(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	if request.method == 'POST':
		checkout_session = stripe.checkout.Session.create(
			payment_method_types = ['card'],
			line_items = [
				{
					'price': settings.PRODUCT_PRICE,
					'quantity': 1,
				},
			],
			mode = 'payment',
			customer_creation = 'always',
			success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
			cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
		)
		return redirect(checkout_session.url, code=303)
	return render(request, 'product_page.html')

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import UserPayment
import stripe
import time

## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	checkout_session_id = request.GET.get('session_id', None)
	session = stripe.checkout.Session.retrieve(checkout_session_id)
	customer = stripe.Customer.retrieve(session.customer)
	user_id = request.user.id
	user_payment = UserPayment.objects.get(app_user=user_id)
	user_payment.stripe_checkout_id = checkout_session_id
	user_payment.save()
	return render(request, 'payment_successful.html', {'customer': customer})


def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	return render(request, 'payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)


# YOUR_DOMAIN="http://127.0.0.1:8000/"
# class CreateCheckoutSessionView(View):
#     def post(self, request, *args, **kwargs):
#         price = Price.objects.get(id=self.kwargs["pk"])
#         domain = "http://127.0.0.1:8000"
#         if settings.DEBUG:
#             domain = "http://127.0.0.1:8000"
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price': price.stripe_price_id,
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/success/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#         )
#         return redirect(checkout_session.url)

 
# class ProductLandingPageView(TemplateView):
#     template_name = "landing.html"
 
#     def get_context_data(self, **kwargs):
#         product = Product.objects.get(name="Test Product")
#         prices = Price.objects.filter(product=product)
#         context = super(ProductLandingPageView,
#                         self).get_context_data(**kwargs)
#         context.update({
#             "product": product,
#             "prices": prices
#         })
#         return context





# class SuccessView(TemplateView):
#     template_name = "success.html"

# class CancelView(TemplateView):
#     template_name = "cancel.html"

# class PaymentAPI(APIView):
#     serializer_class = CardInformationSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         response = {}
#         if serializer.is_valid():
#             data_dict = serializer.validated_data
#             stripe.api_key = 'sk_test_51OoMmqIOAl4JyRuqndcC1R1nSAeorAawIaf1zeAHKO0n65J0e6EF1vNbVJS2M80PjZyZ7zsxx2gKFwqpKBxRSYWK00MoKNwDtN'
#             response = self.stripe_card_payment(data_dict=data_dict)
#         else:
#             response = {
#                 'errors': serializer.errors,
#                 'status': status.HTTP_400_BAD_REQUEST
#             }
#         return Response(response)

#     def stripe_card_payment(self, data_dict):
#         try:
#             card_details = {
#                 "type": "card",
#                 "card": {
#                     "number": data_dict['card_number'],
#                     "exp_month": data_dict['expiry_month'],
#                     "exp_year": data_dict['expiry_year'],
#                     "cvc": data_dict['cvc'],
#                 }
#             }

#             # Create a PaymentMethod using the card details
#             payment_method = stripe.PaymentMethod.create(
#                 type="card",
#                 card=card_details['card']
#             )

#             # Create a PaymentIntent using the PaymentMethod ID
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=10000,  # You can also get the amount from the database by creating a model
#                 currency='inr',
#                 payment_method=payment_method.id,
#                 confirm=True
#             )

#             if payment_intent.status == 'succeeded':
#                 response = {
#                     'message': "Card Payment Success",
#                     'status': status.HTTP_200_OK,
#                     "card_details": card_details,
#                     "payment_intent": payment_intent
#                 }
#             else:
#                 response = {
#                     'message': "Card Payment Failed",
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     "card_details": card_details,
#                     "payment_intent": payment_intent
#                 }
#         except stripe.error.CardError as e:
#             response = {
#                 'error': e.user_message,
#                 'status': status.HTTP_400_BAD_REQUEST
#             }
#         except Exception as e:
#             response = {
#                 'error': "An error occurred",
#                 'status': status.HTTP_400_BAD_REQUEST
#             }
#         return response


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)


# def paymob(request):
#     API_KEY = "ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2T1RZMU5qRTFMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkueXRFb0RDRVl1V1lQaEFPc01CYzFabktwaXRyMkNfLTNTMlVCUXdTQkEzOUt6b1ZIdlFOQ09zX3p6X19GalNjV3l3X2E4dl9TMk0tZVA5eFZsTS1yMFE="
#     accept = AcceptAPI(API_KEY)
#     # Authentication Request
#     auth_token = accept.retrieve_auth_token()
#     print(auth_token)

#     # Order Registration
#     OrderData = {
#         "auth_token": auth_token,
#         "delivery_needed": "false",
#         "amount_cents": "1100",
#         "currency": "EGP",
#         "merchant_order_id": 125,  # UNIQUE
#         "items": [
#             {
#                 "name": "ASC1515",
#                 "amount_cents": "500000",
#                 "description": "Smart Watch",
#                 "quantity": "1"
#             },
#             {
#                 "name": "ERT6565",
#                 "amount_cents": "200000",
#                 "description": "Power Bank",
#                 "quantity": "1"
#             }
#         ],
#         # "shipping_data": {
#         #     "apartment": "803",
#         #     "email": "claudette09@exa.com",
#         #     "floor": "42",
#         #     "first_name": "Clifford",
#         #     "street": "Ethan Land",
#         #     "building": "8028",
#         #     "phone_number": "+86(8)9135210487",
#         #     "postal_code": "01898",
#         #     "extra_description": "8 Ram , 128 Giga",
#         #     "city": "Jaskolskiburgh",
#         #     "country": "CR",
#         #     "last_name": "Nicolas",
#         #     "state": "Utah"
#         # },
#         # "shipping_details": {
#         #     "notes": " test",
#         #     "number_of_packages": 1,
#         #     "weight": 10,
#         #     "weight_unit": "Kilogram",
#         #     "length": 100,
#         #     "width": 100,
#         #     "height": 100,
#         #     "contents": "product of some sorts"
#         # }
#     }
#     order = accept.order_registration(OrderData)
#     print(order)

#     # Payment Key Request
#     Request = {
#         "auth_token": auth_token,
#         "amount_cents": "1500",
#         "expiration": 3600,
#         "order_id": order.get("id"),
#         "billing_data": {
#             "apartment": "803",
#             "email": "claudette09@exa.com",
#             "floor": "42",
#             "first_name": "Clifford",
#             "street": "Ethan Land",
#             "building": "8028",
#             "phone_number": "+86(8)9135210487",
#             "shipping_method": "PKG",
#             "postal_code": "01898",
#             "city": "Jaskolskiburgh",
#             "country": "CR",
#             "last_name": "Nicolas",
#             "state": "Utah"
#         },
#         "currency": "EGP",
#         "integration_id": 4538949,  # https://accept.paymob.com/portal2/en/PaymentIntegrations
#         "lock_order_when_paid": "false"
#     }
#     payment_token = accept.payment_key_request(Request)
#     print(payment_token)

#     # Payments API [Kiosk, Mobile Wallets , Cash, Pay With Saved Token]
#     identifier = "cash"
#     payment_method = "CASH"
#     transaction = accept.pay(identifier, payment_method, payment_token)
#     print(transaction)

#     # Auth-Capture Payments
#     transaction00 = accept.capture_transaction(transaction_id="7608793", amount_cents=1000)
#     print(transaction00)

#     # Refund Transaction
#     transaction01 = accept.refund_transaction(transaction_id="7608793", amount_cents=10)
#     print(transaction01)

#     # Void Transaction
#     transaction02 = accept.void_transaction(transaction_id="7608793")
#     print(transaction02)

#     # Retrieve Transaction
#     transaction03 = accept.retrieve_transaction(transaction_id="7608793")
#     print(transaction03)

#     # Inquire Transaction
#     transaction_inquire = accept.inquire_transaction(merchant_order_id="123", order_id="10883471")
#     print(transaction_inquire)

#     # # Tracking
#     # order_10883471_track = accept.tracking(order_id="832017")
#     # print(order_10883471_track)

#     # Preparing Package
#     # This will return a pdf file url to be printed.
#     package = accept.preparing_package(order_id="832017")
#     print(package)

#     # IFrame URL
#     iframeURL = accept.retrieve_iframe(iframe_id="832017", payment_token=payment_token)
#     print(iframeURL)

#     # Loyalty Checkout
#     response = accept.loyalty_checkout(transaction_reference='', otp='123', payment_token=payment_token)
    
#     print(response)

    
    
#     # return render(request, 'pay.html',
#     #                   {"payment_token": payment_token }) 




# import json
# import requests
# from django.conf import settings
# from django.shortcuts import redirect

# def first_step(request):
#     API_KEY = settings.PAYMOB_API_KEY
#     PAYMOB_API_KEY = "ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2T1RZMU5qRTFMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkueXRFb0RDRVl1V1lQaEFPc01CYzFabktwaXRyMkNfLTNTMlVCUXdTQkEzOUt6b1ZIdlFOQ09zX3p6X19GalNjV3l3X2E4dl9TMk0tZVA5eFZsTS1yMFE="
#     API=PAYMOB_API_KEY
#     accept = AcceptAPI(API_KEY)

#     token = accept.retrieve_auth_token()

#     # API = settings.PAYMOB_API_KEY
#     integrationID = 4538949

#     # First Step: Retrieve Auth Token
#     data = {
#         "api_key": API
#     }
#     # Authentication Request
#     print(token)

#     response = requests.post('https://accept.paymob.com/api/auth/token', json=data)
#     if response.status_code != 200:
#         # Handle error response
#         print(f"Error retrieving auth token: {response.text}")
#         # return redirect('error_page')  # Redirect to an error page or display an error message

#     try:
#         token = response.json()['token']
#     except json.JSONDecodeError:
#         # Handle empty or non-JSON response
#         print(f"Invalid JSON response: {response.text}")
#         # return redirect('error_page')

#     # Second Step: Order Registration
#     data = {
#         "auth_token": token,
#         "delivery_needed": "false",
#         "amount_cents": "100",
#         "currency": "EGP",
#         "items": []
#     }

#     response = requests.post('https://accept.paymob.com/api/ecommerce/orders', json=data)
#     order_id = response.json()['id']

#     # Third Step: Payment Key Request
#     data = {
#         "auth_token": token,
#         "amount_cents": "100",
#         "expiration": 3600,
#         "order_id": order_id,
#         "billing_data": {
#             "apartment": "803",
#             "email": "claudette09@exa.com",
#             "floor": "42",
#             "first_name": "Clifford",
#             "street": "Ethan Land",
#             "building": "8028",
#             "phone_number": "+86(8)9135210487",
#             "shipping_method": "PKG",
#             "postal_code": "01898",
#             "city": "Jaskolskiburgh",
#             "country": "CR",
#             "last_name": "Nicolas",
#             "state": "Utah"
#         },
#         "currency": "EGP",
#         "integration_id": integrationID
#     }

#     response = requests.post('https://accept.paymob.com/api/acceptance/payment_keys', json=data)
#     payment_token = response.json()['token']

#     # Redirect to Payment Page
#     return redirect(f"https://accept.paymob.com/api/acceptance/iframes/452689?payment_token={payment_token}")