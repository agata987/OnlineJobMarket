from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *


def my_account(request):
    return render(request, 'jobSite_app/myAccount.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelnienie zakończyło się sukcesem.')
                else:
                    return HttpResponse('Konto jest zablokowane.')
            else:
                return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
    else:
        form = LoginForm()
    return render(request, 'jobSite_app/login.html', {'form': form})


def dashboard(request):
    offers = JobOffer.objects.all()
    return render(request,'jobSite_app/dashboard.html',{'section':'dashboard', 'offers':offers})


def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)     # utworzenie nowego obiektu uzytkownika, ale jeszcze nie zapisujemy go w bazie danych
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()    # zapisanie obiektu user
            return render(request,'jobSite_app/register_done.html',{'new_user':new_user})
    else:
        user_form = RegisterForm()
    return render(request,'jobSite_app/register.html',{'user_form':user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Uaktualnienie profilu zakończyło się sukcesem.')
        else:
            messages.error(request, 'Wystąpił błąd podczas uaktualniania profilu.')
    else:
        user_form = UserEditForm(instance = request.user)
    return render(request, 'jobSite_app/edit.html',{'user_form':user_form})


def offer_detail(request, id):
    try:
        offer = JobOffer.objects.get(pk=id)
        cities = City.objects.all()
        countries = Country.objects.all()
        employee = User.objects.get(pk=offer.id_employee_id)
        users = User.objects.all()      # poprawic tak zeby nie trzeba bylo pobierac wszystkich uzytkownikow

        try:
            comments = Comment.objects.get(id_job_offer_id=offer.id)
        except Comment.DoesNotExist:
            return render(request, 'jobSite_app/offer_detail.html', {'offer':offer, 'cities':cities, 'countries':countries, 'employee':employee, 'users':users})

    except JobOffer.DoesNotExist:
        raise Http404("Ta oferta nie istnieje.")
    return render(request, 'jobSite_app/offer_detail_com.html', {'offer':offer, 'cities':cities, 'countries':countries, 'employee':employee,'comments':comments})


@login_required
def my_offers_detail(request):
    try:
        offers = JobOffer.objects.filter(id_employee_id = request.user.id)

        try:
            cities = City.objects.all()
        except City.DoesNotExist:
            cities = None
        
        try:
            countries = Country.objects.all()
        except Country.DoesNotExist:
            countries = None

    except JobOffer.DoesNotExist:
        offers = None
        cities = None
        countries = None

    return render(request, 'jobSite_app/my_offers_detail.html', {'offers':offers, 'cities':cities, 'countries':countries})


@login_required
def my_offers(request):
    try:
        my_offers = JobOffer.objects.filter(id_employee_id = request.user.id)
    except JobOffer.DoesNotExist:
        my_offers = None
    
    return render(request, 'jobSite_app/my_offers.html', {'my_offers':my_offers})

def create_offer(request):
    
    if request.method == 'POST':
        offer_form = CreateOfferForm(request.POST)

        if offer_form.is_valid():
            try:
                country = Country.objects.get(name=offer_form.cleaned_data['country'])
            except Country.DoesNotExist:
                country = Country(name=offer_form.cleaned_data['country'])
                country.save()

            try:
                city = City.objects.get(name=offer_form.cleaned_data['city'])
            except City.DoesNotExist:
                city = City(name = offer_form.cleaned_data['city'], id_country = country)
                city.save()

            jobOffer = JobOffer(name=offer_form.cleaned_data['name'],id_employee=request.user,company=offer_form.cleaned_data['company'],full_time=offer_form.cleaned_data['full_time'],remote=offer_form.cleaned_data['remote'],description=offer_form.cleaned_data['description'],id_city=city,min_salary=offer_form.cleaned_data['min_salary'],max_salary=offer_form.cleaned_data['max_salary'])
            jobOffer.save()
            return render(request, 'jobSite_app/offer_created.html')
        else:
            return HttpResponse("offer not valid")
    else:
        offer_form = CreateOfferForm()
        return render(request, 'jobSite_app/create_offer.html', {'offer_form':offer_form})
