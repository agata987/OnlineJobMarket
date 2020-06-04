from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from itertools import chain



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


def is_valid_(param):
    return param != '' and param != "Wybierz..." and param is not None


def dashboard(request):
    offers = JobOffer.objects.all()
    cities = City.objects.all()
    countries = Country.objects.all()

    # filtry

    offer_name_query = request.GET.get('offer_name')
    company_query = request.GET.get('company')


    if is_valid_(offer_name_query):
        offers = offers.filter(name__icontains=offer_name_query)

    if is_valid_(company_query):
        offers = offers.filter(company__icontains=company_query)

    category_name = request.GET.get('category')

    if is_valid_(category_name):
        for cat_num, cat_name in CATEGORY_CHOICES:
            if cat_name == category_name:
                offers = offers.filter(category=cat_num)
                break
    

    city_name = request.GET.get('city')

    if is_valid_(city_name):
        for city2 in cities:
            if city2.name == city_name:
                offers = offers.filter(id_city_id=city2.id)
                break
    
    min_salary_ = request.GET.get('minSalary')

    if is_valid_(min_salary_):
        offers = offers.filter(min_salary__gte=min_salary_)

    not_full_time_ = request.GET.get('not_full_time')

    if not_full_time_ == 'on':
        offers = offers.filter(full_time = 0)
    
    remote_ = request.GET.get('remote')

    if remote_ == 'on':
        offers = offers.filter(remote = 1)

    # to musi byc na koncu, lista nie ma atrybutu "filter"

    country_name = request.GET.get('country')

    if is_valid_(country_name):
        for country2 in countries:
            if country2.name == country_name:
                cities2 = cities.filter(id_country_id = country2.id)

                queries = []
                combined_q = None

                for offer in offers:
                    for city2 in cities2:
                        if offer.id_city_id == city2.id:
                            if city2.name != "Inne":
                                queries.append(offer)

                offers = queries

                break



    return render(request,'jobSite_app/dashboard.html',{'section':'dashboard', 'offers':offers, 'cities':cities, 'categories':CATEGORY_CHOICES, 'countries':countries})


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

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            job_offer = JobOffer.objects.get(pk=id)
            comment = Comment(text=comment_form.cleaned_data['text'],id_job_offer=job_offer,id_user=request.user)
            comment.save()
    else:
        comment_form = CommentForm()

    try:
        offer = JobOffer.objects.get(pk=id)
        cities = City.objects.all()
        countries = Country.objects.all()
        employee = User.objects.get(pk=offer.id_employee_id)
        users = User.objects.all()      # poprawic tak zeby nie trzeba bylo pobierac wszystkich uzytkownikow

        try:
            comments = Comment.objects.filter(id_job_offer_id=offer.id)
        except Comment.DoesNotExist:
            comments = None

    except JobOffer.DoesNotExist:
        raise Http404("Ta oferta nie istnieje.")
    return render(request, 'jobSite_app/offer_detail.html', {'offer':offer, 'cities':cities, 'countries':countries, 'employee':employee,'comments':comments, 'categories':CATEGORY_CHOICES,'comment_form':comment_form,'users':users})



@login_required
def my_offers(request):
    try:
        my_offers = JobOffer.objects.filter(id_employee_id = request.user.id)
    except JobOffer.DoesNotExist:
        my_offers = None
    
    return render(request, 'jobSite_app/my_offers.html', {'my_offers':my_offers})


@login_required
def create_offer(request):
    
    if request.method == 'POST':
        offer_form = CreateOfferForm(request.POST)

        if offer_form.is_valid():
            # try:
            #     country = Country.objects.get(name=offer_form.cleaned_data['country'])
            # except Country.DoesNotExist:
            #     country = Country(name=offer_form.cleaned_data['country'])
            #     country.save()

            # try:
            #     city = City.objects.get(name=offer_form.cleaned_data['city'])
            # except City.DoesNotExist:
            #     city = City(name = offer_form.cleaned_data['city'], id_country = country)
            #     city.save()

            city = City.objects.get(name=offer_form.cleaned_data['city'])


            jobOffer = JobOffer(name=offer_form.cleaned_data['name'],id_employee=request.user,company=offer_form.cleaned_data['company'],category=offer_form.cleaned_data['category'], full_time=offer_form.cleaned_data['full_time'],remote=offer_form.cleaned_data['remote'],description=offer_form.cleaned_data['description'],id_city=city,min_salary=offer_form.cleaned_data['min_salary'],max_salary=offer_form.cleaned_data['max_salary'])
            jobOffer.save()
            return redirect(my_offers)
        else:
            return HttpResponse("offer not valid")
    else:
        offer_form = CreateOfferForm()
        return render(request, 'jobSite_app/create_offer.html', {'offer_form':offer_form})



@login_required
def edit_offer(request, id):
    offer = JobOffer.objects.get(id=id)

    if request.method == 'POST':
        edit_form = EditOfferForm(request.POST)

        if edit_form.is_valid():
            
            #  edytowanie oferty
            full_time = edit_form.cleaned_data['full_time']
            remote = edit_form.cleaned_data['remote']
            description = edit_form.cleaned_data['description']
            min_salary = edit_form.cleaned_data['min_salary']
            max_salary = edit_form.cleaned_data['max_salary']

            offer = JobOffer.objects.filter(pk=id).update(full_time=full_time,remote=remote,description=description,min_salary=min_salary,max_salary=max_salary)


            try:
                offer = JobOffer.objects.get(pk=id)
                cities = City.objects.all()
                countries = Country.objects.all()
                employee = User.objects.get(pk=offer.id_employee_id)
                users = User.objects.all()      # poprawic tak zeby nie trzeba bylo pobierac wszystkich uzytkownikow

                try:
                    comments = Comment.objects.get(id_job_offer_id=offer.id)
                except Comment.DoesNotExist:
                    return render(request, 'jobSite_app/offer_detail.html', {'offer':offer, 'cities':cities, 'countries':countries, 'employee':employee, 'users':users, 'categories':CATEGORY_CHOICES})
            except JobOffer.DoesNotExist:
                raise Http404("Ta oferta nie istnieje.")
    else:
        edit_form = EditOfferForm()
        offer = JobOffer.objects.get(id=id)

        # wartosci poczatkowe formularza
        edit_form.fields['full_time'].initial = offer.full_time
        edit_form.fields['remote'].initial = offer.remote
        edit_form.fields['description'].initial = offer.description
        edit_form.fields['min_salary'].initial = offer.min_salary
        edit_form.fields['max_salary'].initial = offer.max_salary

        return render(request, 'jobSite_app/edit_offer.html', {'edit_form':edit_form, 'offer':offer, 'categories':CATEGORY_CHOICES})


@login_required
def delete_offer(request,id):
    offer = JobOffer.objects.filter(id=id).delete()
    
    return redirect(my_offers)