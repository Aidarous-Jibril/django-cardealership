# dealership/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, Profile, Reservation
from .forms import ProfileForm, CarFilterForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator #for pagination
from django.utils import timezone
from django.contrib import messages


# Define the number of cars per page
CARS_PER_PAGE = 6

def home_view(request):
    form = CarFilterForm(request.GET or None)
    cars = Car.objects.all()

    if form.is_valid():
        if form.cleaned_data['make']:
            cars = cars.filter(make=form.cleaned_data['make'])
        if form.cleaned_data['model']:
            cars = cars.filter(model=form.cleaned_data['model'])
        if form.cleaned_data['fuel']:
            cars = cars.filter(fuel=form.cleaned_data['fuel'])
        if form.cleaned_data['gearbox']:
            cars = cars.filter(gearbox=form.cleaned_data['gearbox'])
        if form.cleaned_data['year']:
            cars = cars.filter(year=form.cleaned_data['year'])
        if form.cleaned_data['price']:
            cars = cars.filter(price=form.cleaned_data['price'])

    paginator = Paginator(cars, CARS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dealership/home.html', {'form': form, 'page_obj': page_obj})

# about view
def about_view(request):
    return render(request, 'about.html')
# FAQ view
def faq_view(request):
    return render(request, 'dealership/faq.html')


# user profile
@login_required
def profile_view(request):
    profile = request.user.profile
    reservations = profile.reservations.all()
    print("Profile:", profile)
    print("Reservations:", reservations)

    return render(request, 'dealership/profile.html', {'profile': profile, 'reservations': reservations})


#car edit user profile view
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('dealership:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'dealership/edit_profile.html', {'form': form})

 
#car details views
def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    #fetch related cars 
    related_cars = Car.objects.filter(make=car.make).exclude(id=car_id)
    return render(request, 'dealership/car_detail.html', {'car': car, 'related_cars': related_cars} )


# Create a view to handle the search query
def car_search_view(request):
    query = request.GET.get('q')
    form = CarFilterForm(request.GET or None)
    cars = Car.objects.all()
    
    if query:
        cars = cars.filter(make__icontains=query) | \
               cars.filter(model__icontains=query) | \
               cars.filter(year__icontains=query)
    
    if form.is_valid():
        if form.cleaned_data['make']:
            cars = cars.filter(make=form.cleaned_data['make'])
        if form.cleaned_data['model']:
            cars = cars.filter(model=form.cleaned_data['model'])
        if form.cleaned_data['fuel']:
            cars = cars.filter(fuel=form.cleaned_data['fuel'])
        if form.cleaned_data['gearbox']:
            cars = cars.filter(gearbox=form.cleaned_data['gearbox'])
        if form.cleaned_data['year']:
            cars = cars.filter(year=form.cleaned_data['year'])
        if form.cleaned_data['price']:
            cars = cars.filter(price=form.cleaned_data['price'])

    paginator = Paginator(cars, CARS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dealership/car_search_results.html', {'form': form, 'page_obj': page_obj, 'query': query})


# Create Reservation view
@login_required
def reserve_car(request, car_id):
    print("Reserve_car view called!")
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        existing_reservation = Reservation.objects.filter(user=request.user, car=car).exists()
        if existing_reservation:
            messages.error(request, 'You have already reserved this car.')
        else:
            ## create reservation
            reservation = Reservation.objects.create(user=request.user, car=car)
            # Associate reservation with user's profile
            request.user.profile.reservations.add(reservation)
            messages.success(request, 'Car reserved successfully!')

        return redirect('dealership:car_detail', car_id=car.id)
    return redirect('dealership:car_detail', car_id=car.id)


#Candel Reservation view
@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        if reservation.user == request.user:
            reservation.delete()
            messages.success(request, 'Reservation cancelled successfully!')
        else:
            messages.error(request, 'You are not authorized to cancel this reservation.')
        return redirect('dealership:profile')
    return redirect('dealership:profile')