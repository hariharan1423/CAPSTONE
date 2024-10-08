from django.shortcuts import render, redirect
from .models import CarSale
import pickle
import numpy as np
import pandas as pd
from .forms import SignupForm, LoginForm


def load():
    with open('App/model.pkl','rb') as file:
        rf_model = pickle.load(file)
    with open('App/encoder.pkl','rb') as en:
        encoder = pickle.load(en)
    with open('App/pca.pkl','rb') as pc:
        pca = pickle.load(pc)
    with open('App/poly.pkl','rb') as po:
        poly = pickle.load(po)
    with open('App/scaler.pkl','rb') as sc:
        scaler = pickle.load(sc)
    return [rf_model,encoder,pca,poly,scaler]

[rf_model,encoder,pca,poly,scaler] = load()

def login(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Validate against the users.txt file
            valid_credentials = False
            with open('users.txt', 'r') as f:
                for line in f:
                    stored_username, stored_email, stored_password = line.strip().split(', ')
                    stored_username = stored_username.split(': ')[1]
                    stored_password = stored_password.split(': ')[1]
                    
                    if username == stored_username and password == stored_password:
                        valid_credentials = True
                        break

            if valid_credentials:
                return redirect('app')  
            else:
                error_message = 'Invalid username or password.'

    else:
        form = LoginForm()

    return render(request, 'APP/login.html', {'form': form, 'error_message': error_message})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            with open('users.txt', 'a') as f:
                f.write(f'Username: {username}, Email: {email}, Password: {password}\n')

            return redirect('app')
    else:
        form = SignupForm()

    return render(request, 'APP/signup.html', {'form': form})



def app(request):
    
    if request.method == 'POST':
        month_year = request.POST.get('year') 
        year = int(month_year.split('-')[0]) 
        name = request.POST.get('name')
        try:
            km_driven = float(request.POST.get('km_driven'))
            mileage = float(request.POST.get('mileage'))
            engine = float(request.POST.get('engine'))
            max_power = float(request.POST.get('max_power'))
            seats = int(request.POST.get('seats'))
            fuel = int(request.POST.get('fuel'))
            seller_type = int(request.POST.get('seller_type'))
            transmission = int(request.POST.get('transmission'))
            owner = request.POST.get('owner')
            state = request.POST.get('state')
            city = request.POST.get('city')
            region = request.POST.get('region')
        except ValueError:
            return render(request,'App/app.html',{"error":"Invalid input. Please ensure all fields are filled out correctly."})

        if (km_driven < 0 or 
            mileage < 0 or 
            engine < 0 or 
            max_power < 0 or 
            seats < 0):
            return render(request,'App/app.html',{"error":"Invalid input. Please ensure all fields are filled out correctly."})

        input = pd.DataFrame([[year, km_driven, fuel, seller_type, transmission, mileage, engine, max_power, seats]], columns=['year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'mileage', 'engine', 'max_power', 'seats'])
 
        X_encoded = encoder.transform(input[['fuel', 'seller_type', 'transmission']]).toarray()

        X_numerical =input[['year', 'km_driven', 'mileage', 'engine', 'max_power', 'seats']].values
        X_combined = np.hstack((X_numerical, X_encoded))


        X_poly = poly.transform(X_combined)

        X_log = np.log(X_combined + 1)  # Adding 1 to avoid log(0)


        X_scaled = scaler.transform(X_combined)

        X_pca = pca.transform(X_combined)

        X_final = np.hstack((X_combined, X_poly, X_log, X_scaled, X_pca))
        prediction = rf_model.predict(X_final)

        print(prediction)
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
            region=region,
            pred_price = prediction
        )
        car_sale.save()

        return render(request,'App/result.html',{'car_sale':car_sale}) 

    return render(request, 'App/app.html')

def result(request):
    return render(request,'App/result.html')