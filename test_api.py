import requests
import json

url = 'http://localhost:5000/predict'
headers = {'Content-type': 'application/json'}
data = { 
    "MSSubClass": 20.0,
    "LotFrontage": 80.0,
    "LotArea": 9600.0,
    "Street": 1.0,
    "Utilities": 0.0,
    "OverallQual": 6.0,
    "OverallCond": 8.0,
    "YearBuilt": 1976.0,
    "YearRemodAdd": 1976.0,
    "MasVnrArea": 0.0,
    "TotalBsmtSF": 1262.0,
    "CentralAir": 1,
    "1stFlrSF": 1262.0,
    "2ndFlrSF": 0.0,
    "LowQualFinSF": 0.0,
    "GrLivArea": 1262.0,
    "BsmtFullBath": 0.0,
    "BsmtHalfBath": 1.0,
    "FullBath": 2.0,
    "HalfBath": 0.0,
    "BedroomAbvGr": 3.0,
    "KitchenAbvGr": 1.0,
    "TotRmsAbvGrd": 6.0,
    "Fireplaces": 1.0,
    "GarageYrBlt": 1976.0,
    "GarageCars": 2.0,
    "GarageArea": 460.0,
    "WoodDeckSF": 298.0,
    "OpenPorchSF": 0.0,
    "EnclosedPorch": 0.0,
    "3SsnPorch": 0.0,
    "ScreenPorch": 0.0,
    "PoolArea": 0.0,
    "MiscVal": 0.0,
    "MoSold": 5.0,
    "YrSold": 2007,
    "ActualPrice": 181500.0  # Agregando el precio real de la vivienda
}
response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")