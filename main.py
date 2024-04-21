import requests


brand = input("Podaj markę samochodu: ")
color = input("Podaj kolor samochodu: ")


car_data = {
    'brand': brand,
    'color': color
}


url = 'http://127.0.0.1:5000/cars'

response = requests.post(url, json=car_data)

if response.status_code == 201:
    print(response.json()['message'])
elif response.status_code == 400:
    print(response.json()['message'])
else:
    print(response.json()['message'])
