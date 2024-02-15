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

from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404, handler500

from django.http import HttpResponse

from django import forms
from .models import UserAdmin, HomeInfo,ProjectManger,ContentCreator
from .forms import AdminForm, LoginForm,HomeInfoForm,ContentCreatorForm

from django.core.cache import cache
from django.views.decorators.cache import cache_page


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
                task = form.instance
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
                p = ProjectManger.objects.create(admin=request.user, task=task, results="output")
                return redirect('/')
            
                        

    


    # form = ContentCreatorForm()
    # return render(request, template_name,
    #               {"homeinfo": homeinfo, "language_code": language_code,
    #                'home_background': home_background,'form':form})





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


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)
