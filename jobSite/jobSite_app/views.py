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
def create_offer(request):
    return render(request, 'jobSite_app/create_offer.html')
