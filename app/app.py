import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np

# COLOR THEME
BG_COLOR        = "#F8FAFC"
CARD_COLOR      = "#FFFFFF"
TEXT_COLOR      = "#0F172A"

PRIMARY_BLUE    = "#1D4ED8"
MID_BLUE        = "#3B82F6"
LIGHT_BLUE      = "#93C5FD"
ORANGE_ACCENT   = "#F59E0B"
GREEN_FORECAST  = "#16A34A"

#  PAGE CONFIG 
st.set_page_config(page_title="Uber Trip Analytics", layout="wide", page_icon="🚕")

# CSS
st.markdown(f"""
<style>
.stApp {{
    background-color: {BG_COLOR};
}}

div[data-testid="metric-container"] {{
    background: linear-gradient(135deg,#ffffff,#f1f5f9);
    padding:18px;
    border-radius:14px;
    border:1px solid #E2E8F0;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);
}}
section[data-testid="stSidebar"] {{
    background-color:#E0E7FF;
}}
</style>
""", unsafe_allow_html=True)

# LOAD DATA 
@st.cache_data
def load_data():
    df = pd.read_csv("../data/Uber-Jan-Feb-FOIL.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["day_name"] = df["date"].dt.day_name()
    df["month"] = df["date"].dt.month_name()
    return df

df = load_data()

# SIDEBAR 
st.sidebar.title("Filters")

months = st.sidebar.multiselect("Month", df["month"].unique(), default=df["month"].unique())
bases  = st.sidebar.multiselect("Base", df["dispatching_base_number"].unique(), default=df["dispatching_base_number"].unique())

filtered_df = df[(df["month"].isin(months)) & (df["dispatching_base_number"].isin(bases))]

#  DOWNLOAD BUTTON 
st.sidebar.markdown("---")
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="uber_filtered_data.csv",
    mime="text/csv"
)

#  TITLE
st.title("🚕 Uber Trip Analytics Dashboard")
st.markdown("Fleet demand analysis & forecasting")

#  KPI SECTION
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

total_trips = int(filtered_df["trips"].sum())
total_vehicles = int(filtered_df["active_vehicles"].sum())
peak_trips = int(filtered_df["trips"].max())
avg_trips_vehicle = round(total_trips / total_vehicles, 2) if total_vehicles else 0

# Growth calculation 
prev_df = df[
    (~df["month"].isin(months)) &
    (df["dispatching_base_number"].isin(bases))
]

prev_trips = prev_df["trips"].sum() if not prev_df.empty else 0
growth = ((total_trips - prev_trips) / prev_trips * 100) if prev_trips > 0 else 0

# KPI CARDS 
col1.metric("Total Trips", f"{total_trips:,}", f"{growth:.1f}% vs prev")
col2.metric("Active Vehicles", f"{total_vehicles:,}")
col3.metric("Peak Daily Trips", f"{peak_trips:,}")
col4.metric("Trips per Vehicle", avg_trips_vehicle)


#  DEMAND TREND
st.subheader("📈 Trip Demand Trend")

trend_df = filtered_df.groupby("date")["trips"].sum().reset_index()

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=trend_df["date"], y=trend_df["trips"],
    mode="lines",
    line=dict(color=PRIMARY_BLUE,width=3),
    fill="tozeroy",
    fillcolor="rgba(29,78,216,0.15)"
))
fig_trend.update_layout(plot_bgcolor=CARD_COLOR,paper_bgcolor=BG_COLOR,font_color=TEXT_COLOR)
st.plotly_chart(fig_trend,use_container_width=True)

# SCATTER 
st.subheader("🚗 Vehicles vs Trips")

fig_scatter = px.scatter(
    filtered_df,x="active_vehicles",y="trips",
    trendline="ols",color_discrete_sequence=[PRIMARY_BLUE]
)
fig_scatter.update_traces(marker=dict(size=9,opacity=0.7,line=dict(width=1,color="white")))
fig_scatter.update_layout(plot_bgcolor=CARD_COLOR,paper_bgcolor=BG_COLOR,font_color=TEXT_COLOR)
st.plotly_chart(fig_scatter,use_container_width=True)

# DAY BAR 
st.subheader("📅 Trips by Day")

order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
day_df=filtered_df.groupby("day_name")["trips"].sum().reset_index()
day_df["day_name"]=pd.Categorical(day_df["day_name"],categories=order,ordered=True)
day_df=day_df.sort_values("day_name")

fig_day=px.bar(day_df,x="day_name",y="trips",color="trips",
               color_continuous_scale=["#DBEAFE","#93C5FD","#3B82F6","#1D4ED8"])
fig_day.update_layout(plot_bgcolor=CARD_COLOR,paper_bgcolor=BG_COLOR,font_color=TEXT_COLOR,coloraxis_showscale=False)
st.plotly_chart(fig_day,use_container_width=True)

# FORECAST
st.subheader("🔮 7 Day Forecast")

trend_df["day_num"]=np.arange(len(trend_df))
model=LinearRegression().fit(trend_df[["day_num"]],trend_df["trips"])

future_X=np.arange(len(trend_df),len(trend_df)+7).reshape(-1,1)
future_preds=model.predict(future_X)
future_dates=pd.date_range(trend_df["date"].iloc[-1],periods=8)[1:]

fig_forecast=go.Figure()
fig_forecast.add_trace(go.Scatter(x=trend_df["date"],y=trend_df["trips"],
                                  mode="lines",line=dict(color=PRIMARY_BLUE,width=3),name="Actual"))
fig_forecast.add_trace(go.Scatter(x=future_dates,y=future_preds,
                                  mode="lines+markers",
                                  line=dict(color=GREEN_FORECAST,dash="dash",width=3),
                                  marker=dict(size=6),name="Forecast"))
fig_forecast.update_layout(plot_bgcolor=CARD_COLOR,paper_bgcolor=BG_COLOR,font_color=TEXT_COLOR)
st.plotly_chart(fig_forecast,use_container_width=True)

st.subheader("🧠 Executive Insights")

best_day = day_df.sort_values("trips",ascending=False).iloc[0]["day_name"]
worst_day = day_df.sort_values("trips").iloc[0]["day_name"]

peak_base = filtered_df.groupby("dispatching_base_number")["trips"].sum().idxmax()

st.success(f"""
📌 **Key Business Insights**

• Highest demand occurs on **{best_day}**  
• Lowest demand occurs on **{worst_day}**  
• Top performing dispatch base: **{peak_base}**  
• Strong positive correlation between vehicles & trips  
• Demand trend indicates steady growth 📈
""")

st.subheader("🏢 Base Performance Heatmap")

heatmap_df = filtered_df.pivot_table(
    values="trips",
    index="dispatching_base_number",
    columns="day_name",
    aggfunc="sum"
)

fig_heat = px.imshow(
    heatmap_df,
    color_continuous_scale="Blues",
    aspect="auto"
)

fig_heat.update_layout(
    plot_bgcolor=CARD_COLOR,
    paper_bgcolor=BG_COLOR,
    font_color=TEXT_COLOR
)

st.plotly_chart(fig_heat,use_container_width=True)

st.subheader("🚨 Trip Spike Detection")

threshold = trend_df["trips"].mean() + 2 * trend_df["trips"].std()
spikes = trend_df[trend_df["trips"] > threshold]

fig_anomaly = go.Figure()

fig_anomaly.add_trace(go.Scatter(
    x=trend_df["date"],
    y=trend_df["trips"],
    mode="lines",
    line=dict(color="#1D4ED8",width=3),
    name="Trips"
))

fig_anomaly.add_trace(go.Scatter(
    x=spikes["date"],
    y=spikes["trips"],
    mode="markers",
    marker=dict(color="red",size=10),
    name="Spike"
))

fig_anomaly.update_layout(
    plot_bgcolor=CARD_COLOR,
    paper_bgcolor=BG_COLOR,
    font_color=TEXT_COLOR
)

st.plotly_chart(fig_anomaly,use_container_width=True)

st.markdown("---")
st.caption("Industry Level Dashboard • Streamlit + Plotly")

