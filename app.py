import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
import plotly.graph_objects as go
from datetime import date
from plotly.subplots import make_subplots
import xml.etree.ElementTree as ET  # <-- import xml parser

st.set_page_config(page_title="📈 Stock Forecast Application", layout="wide")
st.title("📈 Stock Price Forecasting")

# ---------------------------------------------
# 📋 USER INPUTS (Main Screen)
# ---------------------------------------------

# Load companies and tickers from XML file
@st.cache_data
def load_companies_from_xml(xml_path=r"./Assets/companies.xml"):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    companies = {}
    for company in root.findall("company"):
        name = company.find("name").text
        ticker = company.find("ticker").text
        companies[name] = ticker
    return companies

companies = load_companies_from_xml()

options = [f"{name} ({ticker})" for name, ticker in companies.items()]
selected = st.selectbox("Select Stock Company", options)
selected_name = selected.split(" (")[0]
selected_ticker = companies[selected_name]

start_date = st.date_input("Start Date", date(2015, 1, 1), min_value=date(2000, 1, 1))
end_date = st.date_input("End Date", date(2025, 1, 1), min_value=start_date)

n_years = st.slider("Forecast Period (Years)", 1, 10)
n_days = n_years * 365

predict_button = st.button("🔮 Predict")

# ---------------------------------------------
# 📦 Load Data
# ---------------------------------------------
@st.cache_data
def load_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    df.reset_index(inplace=True)
    return df

# ---------------------------------------------
# 🔮 Forecast Logic (Executed only on button click)
# ---------------------------------------------
if predict_button:
    st.subheader(f"📥 Loading data for {selected_name}")
    data = load_data(selected_ticker, start_date, end_date)

    # Show loaded data info
    st.write(f"### Raw Data from {start_date} to {end_date} ({len(data)} rows)")
    st.dataframe(data)

    if data.empty:
        st.error("No data was fetched for this ticker and date range. Please adjust your inputs.")
    else:
        csv_raw = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Raw Data as CSV",
            data=csv_raw,
            file_name=f"{selected_ticker}_raw_data.csv",
            mime='text/csv'
        )

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel('Ticker')

        df = data[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
        df = df.dropna()

        if len(df) < 2:
            st.error("Not enough valid data points to train the forecasting model. Please select a longer date range or a different stock.")
        else:
            model = Prophet(daily_seasonality=True)
            model.fit(df)

            future = model.make_future_dataframe(periods=n_days)
            forecast = model.predict(future)

            st.write("### 📊 Forecast Data")

            forecast_future = forecast[forecast['ds'] > df['ds'].max()]
            st.dataframe(forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

            csv_forecast = forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Forecast Data as CSV",
                data=csv_forecast,
                file_name=f"{selected_ticker}_forecast.csv",
                mime='text/csv'
            )

            # ---------------------------------------------
            # 📈 Forecast Plot (with Gridlines)
            # ---------------------------------------------
            st.subheader("📈 Forecast Plot")

            fig = go.Figure()

            fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], mode='lines', name='Actual', line=dict(color='red')))
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], line=dict(width=0), showlegend=False))
            fig.add_trace(go.Scatter(
                x=forecast['ds'], y=forecast['yhat_lower'],
                fill='tonexty', fillcolor='rgba(0, 123, 255, 0.2)',
                line=dict(width=0), name='Confidence Interval'
            ))

            fig.update_layout(
                title=f"{selected_name} Stock Price Forecast",
                xaxis=dict(title="Date", showgrid=True, gridcolor='lightgray'),
                yaxis=dict(title="Price (USD)", showgrid=True, gridcolor='lightgray'),
                template="simple_white",
                hovermode="x unified",
                margin=dict(l=30, r=30, t=50, b=30)
            )

            st.plotly_chart(fig, use_container_width=True)

            # ---------------------------------------------
            # 📉 Forecast Components (Interactive)
            # ---------------------------------------------
            with st.expander("📉 Show Forecast Components (Trend, Yearly, etc.)"):
                st.subheader("📊 Forecast Components (Interactive)")

                fig_components = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=("Trend", "Yearly Seasonality")
                )

                fig_components.add_trace(
                    go.Scatter(x=forecast['ds'], y=forecast['trend'], mode='lines', name='Trend', line=dict(color='blue')),
                    row=1, col=1
                )

                if 'yearly' in forecast.columns:
                    fig_components.add_trace(
                        go.Scatter(x=forecast['ds'], y=forecast['yearly'], mode='lines', name='Yearly Seasonality', line=dict(color='orange')),
                        row=2, col=1
                    )
                else:
                    fig_components.add_annotation(
                        text="Yearly seasonality not available",
                        xref="paper", yref="paper",
                        x=0.5, y=0.25, showarrow=False, font=dict(size=14)
                    )

                fig_components.update_layout(
                    height=600,
                    showlegend=False,
                    template="plotly_white",
                    xaxis=dict(title="Date"),
                    yaxis=dict(title="Trend"),
                    xaxis2=dict(title="Date"),
                    yaxis2=dict(title="Yearly Seasonality"),
                    margin=dict(t=40, b=40, l=30, r=30)
                )

                st.plotly_chart(fig_components, use_container_width=True)
