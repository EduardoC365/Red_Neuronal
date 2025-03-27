from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import pandas as pd
import joblib

app = Flask(__name__)

# Cargar el modelo Keras
try:
    model = tf.keras.models.load_model('modelos/modelo_3.keras')
    print("Modelo cargado correctamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model = None

# Campos requeridos para la entrada del modelo
REQUIRED_FIELDS = [
    "MSSubClass", "LotFrontage", "LotArea", "Street", "Utilities", "OverallQual",
    "OverallCond", "YearBuilt", "YearRemodAdd", "MasVnrArea", "TotalBsmtSF",
    "CentralAir", "1stFlrSF", "2ndFlrSF", "LowQualFinSF", "GrLivArea", "BsmtFullBath",
    "BsmtHalfBath", "FullBath", "HalfBath", "BedroomAbvGr", "KitchenAbvGr",
    "TotRmsAbvGrd", "Fireplaces", "GarageYrBlt", "GarageCars", "GarageArea",
    "WoodDeckSF", "OpenPorchSF", "EnclosedPorch", "3SsnPorch", "ScreenPorch",
    "PoolArea", "MiscVal", "MoSold", "YrSold"
]

# Cargar transformadores
try:
    scaler = joblib.load('archivos_transformers/transformer.pkl')
    scaler_precio = joblib.load('archivos_transformers/price_transformer.pkl')
    print("Transformadores cargados correctamente.")
except Exception as e:
    print(f"Error al cargar los transformadores: {e}")
    scaler, scaler_precio = None, None

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or scaler is None or scaler_precio is None:
        return jsonify({'error': 'Modelo o transformadores no cargados.'}), 500

    try:
        data = request.get_json()
        
        # Validar presencia de los campos requeridos
        missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
        if missing_fields:
            return jsonify({'error': f'Campos faltantes: {missing_fields}'}), 400
        
        # Extraer el precio real si está presente
        actual_price = data.pop("ActualPrice", None)
        
        # Crear DataFrame con los datos de entrada
        input_data = pd.DataFrame([data])
        
        # Aplicar transformación
        input_data_scaled = scaler.transform(input_data)
        input_data_scaled = pd.DataFrame(input_data_scaled, columns=REQUIRED_FIELDS)
        
        # Realizar predicción
        prediction = model.predict(input_data_scaled)
        predicted_price = float(scaler_precio.inverse_transform(prediction)[0][0])
        
        # Construir la respuesta asegurando que todos los valores sean float
        response = {"Predicción del precio de la vivienda": predicted_price}
        
        if actual_price is not None:
            actual_price = float(actual_price)
            response["Precio real"] = actual_price
            response["Diferencia"] = round(actual_price - predicted_price, 2)
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error en la predicción: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
