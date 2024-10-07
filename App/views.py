from django.shortcuts import render, redirect
from .models import CarSale


def app(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        year = request.POST.get('year')
        km_driven = request.POST.get('km_driven')
        state = request.POST.get('state')
        city = request.POST.get('city')
        fuel = request.POST.get('fuel')
        seller_type = request.POST.get('seller_type')
        transmission = request.POST.get('transmission')
        owner = request.POST.get('owner')
        mileage = request.POST.get('mileage')
        engine = request.POST.get('engine')
        max_power = request.POST.get('max_power')
        seats = request.POST.get('seats')
        region = request.POST.get('region')

        # Create a new CarSale instance
        car_sale = CarSale(
            name=name,
            year=year,
            km_driven=km_driven,
            state=state,
            city=city,
            fuel=fuel,
            seller_type=seller_type,
            transmission=transmission,
            owner=owner,
            mileage=mileage,
            engine=engine,
            max_power=max_power,
            seats=seats,
            region=region
        )
        car_sale.save()
        return render(request,'App/result.html',{'car_sale':car_sale}) 

    return render(request, 'App/app.html')

def result(request):
    return render(request,'App/result.html')