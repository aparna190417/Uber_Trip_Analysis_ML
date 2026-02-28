# 🚖 Uber Trip Demand using Machine Learning

This project analyzes Uber trip demand and builds advanced machine learning models to forecast daily trip volume using operational and time-based features.

Along with ML modeling, the project also includes:
• Interactive Python Dashboard (Streamlit)  
• Professional Power BI Dashboard  

This makes the project a **complete end-to-end Data Analytics + Machine Learning project.**

---

## 📌 Project Overview
Ride-sharing companies rely heavily on demand forecasting to manage fleet supply, reduce waiting time, and optimize operations.

In this project we:
• Analyze Uber trip demand patterns  
• Perform feature engineering & time-series validation  
• Train multiple ML models  
• Compare model performance  
• Build an Ensemble forecasting model  
• Deploy insights through dashboards  

---

## 🧰 Tech Stack
Python • Pandas • NumPy • Matplotlib • Seaborn  
Scikit-Learn • XGBoost • Streamlit • Power BI  

---

## 📂 Dataset
Uber TLC FOIL Dataset (NYC Uber Trips)

Features used:
- date
- trips (Target Variable)
- active_vehicles
- weekday
- month
- day

---

## 🔍 Exploratory Data Analysis (EDA)

The goal of EDA was to understand demand behaviour, supply patterns, and hidden trends before building ML models.

- Key Analysis Performed

### Demand & Trend Analysis
- Daily trip demand trend visualization
- 7-Day moving average to smooth volatility
- Identification of demand spikes and seasonal patterns

### Supply vs Demand Analysis
- Active vehicles trend analysis
- Trips vs Active Vehicles correlation analysis
- Fleet utilization behaviour during peak demand

### Time-Based Pattern Discovery
- Weekday-wise demand distribution
- Monthly demand comparison (Jan vs Feb)
- Week-wise trend analysis for short-term seasonality

### Correlation & Feature Insights

- Correlation heatmap to identify important predictors
- Strong relationship observed between trips and active vehicles
- Time-based features proved highly predictive for forecasting

📁 All EDA charts are saved in: **images/eda/**


---

## 🤖 Machine Learning Pipeline

### ⏱ Time-Series Validation
Used **TimeSeriesSplit** instead of random split to prevent data leakage and simulate real-world forecasting.

### 🧠 Models Trained
| Model | Purpose |
|---|---|
| Random Forest | Baseline model |
| Gradient Boosting | Boosting model |
| XGBoost | Best performing model ⭐ |
| Ensemble Model | Combined predictions |

### 📊 Model Evaluation Metrics
• MAE (Mean Absolute Error)  
• RMSE (Root Mean Squared Error)  
• R² Score  

### 🏆 Best Model
XGBoost achieved the best performance among individual models.  
An **Ensemble Model** improved prediction stability and reliability.

📁 Charts saved in **images/ml**

---

## 📉 Ensemble Modeling

Final prediction combines models:

```
Ensemble = 40% XGBoost + 30% RandomForest + 30% GradientBoosting
```

This improves prediction stability and reduces model variance.

---

## 📊 Key Insights

• Uber demand shows strong weekly patterns.  
• Active vehicles closely follow trip demand.  
• Demand shows high day-to-day volatility.  
• Time-series validation improves real-world reliability.  
• Ensemble modeling provides more stable predictions.

---

## 🖥 Python Interactive Dashboard (Streamlit)

An analytical dashboard built using Streamlit + Plotly.

### Features:
• KPI cards (Trips, Vehicles, Peak Day)  
• Demand trend with moving average  
• Trips vs Vehicles relationship  
• Weekday & Monthly demand analysis  
• Forecast visualization  

📁 File: **app/app.py**

---

## 📊 Power BI Dashboard

A professional interactive dashboard with multiple pages:

### Pages Included:
• Overview (KPIs, Trends, Weekday Patterns)  
• Base Analysis (Contribution, Heatmaps)  
• Prediction (Forecast & Key Influencers)

📁 File: **PowerBi_Dashboard/Uber_Trip_Analysis_Dashboard.pbix**

---

## 📁 Folder Structure

```
Uber-Trip-Analysis-ML/
│
├── PowerBi_Dashboard/
├── app/
├── data/
├── images/
│   ├── eda/
│   └── ml/
├── notebook/
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run the Project

### 1️⃣ Clone Repository
```
git clone https://github.com/aparna190417/Uber-Trip-Analysis-ML.git
cd Uber-Trip-Analysis-ML
```

### 2️⃣ Install Requirements
```
pip install -r requirements.txt
```

### 3️⃣ Run Notebook
```
jupyter notebook
```
Open → `notebook/Uber_Trip_Analysis_ML.ipynb`

### 4️⃣ Run Streamlit Dashboard
```
cd app
streamlit run app.py
```

### 5️⃣ Open Power BI Dashboard
Open:
`PowerBi_Dashboard/Uber_Trip_Analysis_Dashboard.pbix`

---

## 🚀 Future Improvements
• Use full-year data for seasonality forecasting  
• Implement ARIMA / Prophet / LSTM models  
• Deploy real-time prediction API  
• Add weather & event data  

---

## 👩‍💻 Author
**Aparna Patel**  
