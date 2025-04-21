# Flood Risk Prediction in Pathum Thani Based on Upstream Water Flow at Bang Sai Gate (C.29A)

This project aims to predict the water discharge at **Bang Sai Gate (C.29A)**, a key water control point near Pathum Thani Province, using upstream environmental data. The goal is to assess **flood risk levels** in the area using machine learning techniques.

## 🌊 Project Overview

Flooding in Pathum Thani is often caused by large volumes of upstream water flowing through the Chao Phraya River, especially through the Bang Sai Gate. To help manage this risk, we developed a prediction system that utilizes historical environmental data from 2020 to 2024 and provides a simple **web application** for users to simulate and forecast flood risk levels.

## 📁 Data Sources

The dataset is composed of three main types of features collected from trusted public APIs and open datasets:

1. **Water Discharge**: Daily discharge values from upstream stations:
   - P.17 (Banphot Phisai)
   - N.67 (Chum Saeng)
   - C.13 (Chai Nat)
   - C.29A (Bang Sai) – Used as target

2. **Rainfall**: Total rainfall from 4 districts:
   - Phak Hai (TCP004)
   - Bang Ban (CPY010)
   - Tha Ruea (48415)
   - Bang Pahan (LBI001)

3. **Weather**:
   - Minimum and Maximum Temperature (°C)
   - Relative Humidity (%)

## 🧠 Model Development

We compared three regression models:

- `Linear Regression`
- `Random Forest Regressor`
- `XGBoost Regressor` ✅ *(Best performance)*

The model was selected based on R² score and RMSE values on the test set.

| Model            | RMSE   | R² Score |
|------------------|--------|----------|
| Linear Regression| 158.37 | 0.9302   |
| Random Forest    | 128.21 | 0.9542   |
| XGBoost          | 116.02 | 0.9625   |

## 🕸️ Web Application

A simple Flask-based web app was developed where users can:

- Auto-fill environmental data from real-time public APIs
- Manually input values to simulate different flood scenarios
- Receive water flow predictions and corresponding flood risk categories

> The web app predicts discharge values at **C.29A** and classifies risk as:
> - Normal: `< 2500 m³/s`
> - Flood Risk: `2500 – 3500 m³/s`
> - Flood: `> 3500 m³/s`

## 📊 Folder Structure

├── app.py
├── data/
│   ├── Data_2020_2024.csv
├── model/
│   ├── XGBoost_model.pkl
│   └── scaler.pkl
├── notebooks/
│   ├── Train_Model.ipynb
├── templates/
│   ├── index.html
│   └── result.html
├── static/
│   └── images/
│       └── flood_map.gif
└── README.md

## 📌 References

- Thai Water Data System: https://www.thaiwater.net
- RID Smart Water Operations Center: https://swoc.rid.go.th
- Hydro-Informatics Institute (HII): https://data.hii.or.th
- News references cited in the academic report
