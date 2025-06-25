import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
import plotly.graph_objects as go
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="📈 Stock Forecast Application", layout="wide")
st.title("📈 Stock Price Forecasting")

st.sidebar.header("User Input Parameters")

companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet Class A": "GOOGL",
    "Alphabet Class C": "GOOG",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "Meta Platforms": "META",
    "NVIDIA": "NVDA",
    "Berkshire Hathaway Class B": "BRK-B",
    "JPMorgan Chase": "JPM",
    "Johnson & Johnson": "JNJ",
    "Visa": "V",
    "Walmart": "WMT",
    "UnitedHealth Group": "UNH",
    "Procter & Gamble": "PG",
    "Mastercard": "MA",
    "Home Depot": "HD",
    "Disney": "DIS",
    "Bank of America": "BAC",
    "PayPal": "PYPL",
    "ExxonMobil": "XOM",
    "Netflix": "NFLX",
    "Adobe": "ADBE",
    "Salesforce": "CRM",
    "Intel": "INTC"
}

# Create dropdown options with full name and ticker
options = [f"{name} ({ticker})" for name, ticker in companies.items()]

selected = st.sidebar.selectbox("Select Stock Company", options)

# Extract ticker and company name separately
selected_name = selected.split(" (")[0]
selected_ticker = companies[selected_name]

start_date = st.sidebar.date_input("Start Date", date(2015, 1, 1), min_value=date(2000, 1, 1))
end_date = st.sidebar.date_input("End Date", date(2025, 1, 1), min_value=start_date)

n_years = st.sidebar.slider("Forecast Period (Years)", 1, 10)
n_days = n_years * 365

predict_button = st.sidebar.button("🔮 Predict")

@st.cache_data
def load_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    df.reset_index(inplace=True)
    return df

if predict_button:
    st.subheader(f"📥 Loading data for {selected_name}")
    data = load_data(selected_ticker, start_date, end_date)

    st.write(f"### Raw Data from {start_date} to {end_date}")
    st.dataframe(data)

    # Download button for raw data
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

    model = Prophet(daily_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=n_days)
    forecast = model.predict(future)

    st.write("### 📊 Forecast Data")

    forecast_future = forecast[forecast['ds'] > df['ds'].max()]
    st.dataframe(forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

    # Download button for forecast data
    csv_forecast = forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Forecast Data as CSV",
        data=csv_forecast,
        file_name=f"{selected_ticker}_forecast.csv",
        mime='text/csv'
    )

    st.subheader("📈 Forecast Plot (Interactive)")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['ds'], y=df['y'], mode='lines', name='Actual',
        line=dict(color='red', width=1)
    ))

    fig.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['yhat_upper'], mode='lines',
        line=dict(width=0), showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=forecast['ds'], y=forecast['yhat_lower'], mode='lines',
        fill='tonexty', fillcolor='rgba(173,216,230,0.2)',
        line=dict(width=0), name='Confidence Interval'
    ))

    fig.update_layout(
        title=dict(text=f"{selected_name} Stock Price Forecast", font=dict(color='black')),
        xaxis=dict(
            title=dict(text="Date", font=dict(color='black')),
            tickfont=dict(color='black'),
            showgrid=True,
            gridcolor='lightgray',
            color='black'
        ),
        yaxis=dict(
            title=dict(text="Price (USD)", font=dict(color='black')),
            tickfont=dict(color='black'),
            showgrid=True,
            gridcolor='lightgray',
            color='black'
        ),
        template="plotly_white",
        hovermode="x unified",
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='black'),
        legend=dict(
            font=dict(color='black'),
            bgcolor='white'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📉 Show Forecast Components (Trend, Yearly, etc.)"):
        fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        sns.lineplot(data=forecast, x='ds', y='trend', ax=axs[0], color='blue')
        axs[0].set_title('Trend')
        axs[0].set_ylabel('Value')

        if 'yearly' in forecast.columns:
            sns.lineplot(data=forecast, x='ds', y='yearly', ax=axs[1], color='orange')
            axs[1].set_title('Yearly Seasonality')
            axs[1].set_ylabel('Value')
        else:
            axs[1].text(0.5, 0.5, "Yearly seasonality not available", ha='center', va='center')
            axs[1].set_title('Yearly Seasonality')
            axs[1].set_ylabel('Value')

        plt.xlabel('Date')
        plt.tight_layout()
        st.pyplot(fig)
