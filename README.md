# Flood Prediction in Pathum Thani Province

This repository contains the implementation and analysis code for the **Flood Prediction Project** using advanced machine learning algorithms to predict flood events in Pathum Thani Province, Thailand.

## Project Overview
The goal of this project is to develop and evaluate predictive models integrating historical flood records and real-time environmental data (meteorological and hydrological) to enhance flood prediction accuracy and response time.

## Data
The datasets used include:
- **Historical Flood Records:** Past flood event details (dates, locations, severity).
- **Meteorological Data:** Rainfall intensity, temperature, humidity, wind speed, atmospheric pressure.
- **Hydrological Data:** Real-time river water levels.
- **Geospatial Data:** Digital Elevation Models (DEM), land use, and infrastructure maps.

## Methodology
The methodology consists of five key stages:
1. **Data Preprocessing:** Data cleaning, normalization, interpolation, dimensionality reduction (PCA).
2. **Model Selection:** Evaluation and comparison of LSTM, XGBoots, and Random Forest models.
3. **Training and Validation:** Dataset splitting (70% training, 30% testing), cross-validation, hyperparameter tuning (Grid Search).
4. **Experimental Analysis:** Scenario-based testing to evaluate model performance using both historical and real-time datasets.
5. **Evaluation Metrics:** Accuracy, F1-score, Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and computational efficiency.

## Repository Structure
```
Flood_Prediction/
│
├── data/              # Dataset files
├── notebooks/         # Jupyter notebooks (modeling and analysis)
├── src/               # Source code for preprocessing and model training
├── results/           # Experimental results and evaluation metrics
├── figures/           # Diagrams and visuals for the project
└── README.md          # Project overview and instructions
```

## Contributors
- Aman Bhardwaj
- Arisa Phanmaneelak
- Noramon Kongoon
- Thilina Senadheera

## References
Please refer to the `Midway Report.pdf` included in this repository for detailed references and further reading.

---
