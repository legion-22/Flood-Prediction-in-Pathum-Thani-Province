from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
import requests

app = Flask(__name__)

# Load model and preprocessing tools
model = joblib.load(r"E:\Jan_2025\ML\Project\Code\Git_ML_Project\model\XGBoost_model.pkl")  # Trained regression model
scaler = joblib.load(r"E:\Jan_2025\ML\Project\Code\Git_ML_Project\model\scaler.pkl")      # Fitted scaler for input features

# Feature order used during training (no label encoding needed now)
feature_names = [
    'Water Station P.17 [m³/s] ',
    'Water Station N.67 [m³/s] ',
    'Water Station C.13 [m³/s] ',
    'Rainfall TCP004 (mm)',
    'Rainfall CPY010 (mm)',
    'Rainfall 48415 (mm)',
    'Rainfall LBI001 (mm)',
    'Min_Temp',
    'Max_Temp',
    'relative humidity (%)'
]

def get_latest_rainfall():
    url = "https://api-v3.thaiwater.net/api/v1/thaiwater30/provinces/rain24?include_zero=1&province_code=14"

    # Mapping target district names to feature names
    target_districts = {
        "Phak Hai District": "Rainfall TCP004 (mm)",
        "Bang Ban District": "Rainfall CPY010 (mm)",
        "Tha Ruea District": "Rainfall 48415 (mm)",
        "Bang Pahan District": "Rainfall LBI001 (mm)"
    }

    # Initialize total rainfall dictionary
    rainfall_totals = {feature: 0.0 for feature in target_districts.values()}

    try:
        response = requests.get(url)
        data = response.json()

        if data["result"] == "OK":
            for item in data["data"]:
                district_en = item["geocode"]["amphoe_name"]["en"]
                rain_value = item.get("rain_24h")

                # Skip if rain_value is missing or None
                if rain_value is None:
                    continue

                if district_en in target_districts:
                    feature_name = target_districts[district_en]
                    rainfall_totals[feature_name] += rain_value

    except Exception as e:
        print(f"[ERROR] Failed to fetch rainfall data: {e}")

    return rainfall_totals

def get_water_discharge():
    url = "https://app.rid.go.th/reservoir/telemetry/api/telemetryGeojson?basin=chaophraya"
    target_terms = {
        "P.17": "Water Station P.17 [m³/s] ",
        "N.67": "Water Station N.67 [m³/s] ",
        "C.13": "Water Station C.13 [m³/s] "
    }

    discharge_data = {label: None for label in target_terms.values()}

    try:
        response = requests.get(url)
        data = response.json()

        for feature in data.get("features", []):
            props = feature.get("properties", {})
            term = props.get("term")

            if term in target_terms:
                label = target_terms[term]
                try:
                    discharge_data[label] = float(props.get("TMD_UStream", 0))
                except:
                    discharge_data[label] = None
    except Exception as e:
        print(f"Error fetching discharge data: {e}")

    return discharge_data

def get_min_max_temperature():
    url = "https://api-v3.thaiwater.net/api/v1/thaiwater30/public/thaiwater/temperature?province_code=14"

    try:
        response = requests.get(url)
        json_data = response.json()
        entries = json_data.get("data", {}).get("data", [])

        temps = [entry["temperature"] for entry in entries if entry.get("temperature") is not None]
        
        if temps:
            return {
                "Min_Temp": min(temps),
                "Max_Temp": max(temps)
            }
    except Exception as e:
        print("Error fetching temperature:", e)

    return {
        "Min_Temp": None,
        "Max_Temp": None
    }

def get_average_humidity():
    url = "https://api-v3.thaiwater.net/api/v1/thaiwater30/public/thaiwater/weather?province_code=14"
    try:
        response = requests.get(url)
        data = response.json()
        humidity_entries = data.get("humid", {}).get("data", [])

        humid_values = [entry["humid"] for entry in humidity_entries if entry.get("humid") is not None]

        if humid_values:
            avg_humidity = sum(humid_values) / len(humid_values)
            return {"relative humidity (%)": round(avg_humidity, 2)}
    except Exception as e:
        print("Error fetching humidity:", e)

    return {"relative humidity (%)": None}

@app.route('/')
def home():
    rainfall_data = get_latest_rainfall()
    discharge_data = get_water_discharge() 
    temperature_data = get_min_max_temperature()
    humidity_data = get_average_humidity()
    print("Rainfall data:", rainfall_data)
    print("Discharge data:", discharge_data)
    print("Temp data:", temperature_data)
    print("Humidity data:", humidity_data)
    return render_template(
        'index.html',
        rainfall_data=rainfall_data,
        discharge_data=discharge_data,
        temperature_data=temperature_data,
        humidity_data=humidity_data
    )

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get inputs from form and convert to floats
        input_data = [float(request.form[name]) for name in feature_names]
        input_array = np.array(input_data).reshape(1, -1)

        # Scale features
        input_scaled = scaler.transform(input_array)

        # Make prediction (regression)
        prediction = model.predict(input_array)[0]

        # Interpret prediction as a flood category
        if prediction < 2500:
            label = "Normal"
        elif 2500 <= prediction <= 3500:
            label = "Flood Risk"
        else:
            label = "Flood"

        return render_template('result.html', prediction_text=f'Predicted Water Flow at Water Station C.29A: {prediction:.2f} m³/s ({label})')
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
