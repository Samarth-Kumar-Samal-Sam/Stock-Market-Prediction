import streamlit as st
from datetime import date
import xml.etree.ElementTree as ET
import yfinance as yf
import pandas as pd

from prophet import Prophet
from neuralprophet import NeuralProphet
import plotly.graph_objects as go

from PIL import Image
import io
import base64

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="💹Stock Price Prediction", layout="wide")

# -----------------------------
# UI / CSS (Premium dark theme + spacing + BUTTON HOVER COLOR ANIMATION + CENTERED FOOTER)
# -----------------------------
st.markdown(
    """
<style>
section.main > div.block-container{
  padding-top: 0.85rem;
  padding-bottom: 1.2rem;
  max-width: 1200px;
}
div.element-container{
  margin-top: 0.35rem !important;
  margin-bottom: 0.35rem !important;
}
.spacer-xs{ height: 8px; }
.spacer-sm{ height: 14px; }
.spacer-md{ height: 22px; }
.spacer-lg{ height: 32px; }

/* ============================
   HERO HEADER
   ============================ */
.hero-wrap{
  position: relative;
  padding: 28px 22px 24px 22px;
  border-radius: 22px;
  overflow: hidden;
  margin-top: 8px;
  margin-bottom: 18px;
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow:
    0 34px 90px rgba(0,0,0,0.65),
    0 0 0 1px rgba(255,255,255,0.05) inset;
  transition: transform 220ms ease, box-shadow 220ms ease;
}
.hero-wrap::before{
  content: "";
  position: absolute;
  inset: -120%;
  background: radial-gradient(1200px 700px at 20% 30%, rgba(64,165,255,0.35), transparent 60%),
              radial-gradient(900px 600px at 80% 40%, rgba(0,210,168,0.28), transparent 55%),
              radial-gradient(800px 500px at 55% 85%, rgba(170,90,255,0.22), transparent 55%),
              linear-gradient(120deg, #0A0F1A 0%, #0B1220 40%, #07111F 100%);
  background-size: 140% 140%;
  animation: heroDrift 10.5s ease-in-out infinite;
}
.hero-wrap::after{
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.35);
  backdrop-filter: blur(14px);
}
.hero-orb{
  position: absolute;
  z-index: 1;
  width: 280px;
  height: 280px;
  border-radius: 999px;
  filter: blur(24px);
  opacity: 0.55;
  animation: orbFloat 7.5s ease-in-out infinite;
}
.orb1{
  top: -120px; left: -90px;
  background: radial-gradient(circle at 30% 30%, rgba(77,150,255,0.85), rgba(77,150,255,0.0) 60%);
}
.orb2{
  bottom: -140px; right: -110px;
  background: radial-gradient(circle at 30% 30%, rgba(0,210,168,0.85), rgba(0,210,168,0.0) 60%);
  animation-delay: 0.8s;
}
.orb3{
  top: 20px; right: 22%;
  width: 210px; height: 210px;
  background: radial-gradient(circle at 30% 30%, rgba(170,90,255,0.75), rgba(170,90,255,0.0) 62%);
  animation-delay: 1.4s;
}
@keyframes orbFloat{
  0%,100% { transform: translate(0,0) scale(1.0); }
  50%     { transform: translate(18px,-14px) scale(1.04); }
}
@keyframes heroDrift{
  0%   { transform: translate(0,0); }
  50%  { transform: translate(45px,-25px); }
  100% { transform: translate(0,0); }
}
.hero-wrap:hover{
  transform: translateY(-2px);
  box-shadow:
    0 44px 110px rgba(0,0,0,0.72),
    0 0 0 1px rgba(255,255,255,0.06) inset;
}
.hero-content{
  position: relative;
  z-index: 2;
  display:flex;
  align-items:center;
  justify-content:center;
  flex-direction:column;
  text-align:center;
}
.hero-logo{
  width: 92px;
  height: 92px;
  border-radius: 18px;
  object-fit: cover;
  box-shadow:
    0 18px 38px rgba(0,0,0,0.55),
    0 0 0 1px rgba(255,255,255,0.10) inset;
  animation: floatIcon 3.4s ease-in-out infinite;
}
@keyframes floatIcon{
  0%,100% { transform: translateY(0); }
  50%     { transform: translateY(-9px); }
}
.hero-title{
  font-size: 46px;
  font-weight: 950;
  letter-spacing: 0.4px;
  margin-top: 12px;
  margin-bottom: 6px;
  background: linear-gradient(90deg, #EAF2FF 0%, #A9D0FF 35%, #BDF7E7 70%, #EAF2FF 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 18px 42px rgba(0,0,0,0.55);
}
.hero-subtitle{
  font-size: 16px;
  margin-top: 0px;
  color: rgba(255,255,255,0.90);
}
.hero-type{
  margin: 12px auto 0 auto;
  font-size: 14px;
  color: rgba(255,255,255,0.95);
  white-space: nowrap;
  overflow: hidden;
  border-right: 2px solid rgba(255,255,255,0.90);
  width: 0;
  max-width: 100%;
  text-align: center;
  animation:
    typing 3.2s steps(72,end) forwards,
    removeCursor 0s forwards 3.2s;
}
@keyframes typing{
  from { width: 0; }
  to   { width: 62ch; }
}
@keyframes removeCursor{
  to { border-right: none; }
}
.hero-line{
  margin-top: 16px;
  height: 3px;
  width: min(620px, 62%);
  border-radius: 999px;
  background: linear-gradient(
    90deg,
    rgba(77,150,255,0.0),
    rgba(77,150,255,0.95),
    rgba(0,210,168,0.95),
    rgba(170,90,255,0.95),
    rgba(77,150,255,0.0)
  );
  background-size: 220% 100%;
  animation: lineSweep 2.8s linear infinite;
  opacity: 0.95;
}
@keyframes lineSweep{
  0%   { background-position: 0% 0%; }
  100% { background-position: 220% 0%; }
}

/* ============================
   INPUT CARDS
   ============================ */
.ui-card{
  position: relative;
  border-radius: 18px;
  padding: 16px 16px 14px 16px;
  border: 1px solid rgba(255,255,255,0.10);
  background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
  box-shadow: 0 18px 44px rgba(0,0,0,0.45);
  overflow: hidden;
  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}
.ui-card::before{
  content:"";
  position:absolute;
  inset:-60%;
  background: radial-gradient(520px 240px at 15% 25%, rgba(77,150,255,0.22), transparent 55%),
              radial-gradient(520px 240px at 90% 85%, rgba(0,210,168,0.16), transparent 60%);
  opacity: 0.9;
  animation: cardDrift 9.5s ease-in-out infinite;
}
@keyframes cardDrift{
  0%   { transform: translate(0,0); }
  50%  { transform: translate(22px,-14px); }
  100% { transform: translate(0,0); }
}
.ui-card:hover{
  transform: translateY(-2px);
  box-shadow: 0 22px 60px rgba(0,0,0,0.55);
  border-color: rgba(77,150,255,0.35);
}
.ui-card-content{ position: relative; z-index: 2; }
.ui-label{
  display:flex;
  align-items:center;
  justify-content:center;
  gap: 8px;
  font-size: 18px;
  font-weight: 900;
  color: rgba(255,255,255,0.94);
  margin: 0 0 10px 0;
  text-align: center;
}
.ui-card [data-baseweb="select"] > div{
  background: rgba(0,0,0,0.25) !important;
  border-color: rgba(255,255,255,0.18) !important;
}
.ui-card input{
  background: rgba(0,0,0,0.25) !important;
  border-color: rgba(255,255,255,0.18) !important;
}
.ui-card [data-baseweb="slider"] [role="slider"]{
  box-shadow: 0 0 0 6px rgba(77,150,255,0.15);
}

/* ============================
   RECOMMENDATION
   ============================ */
.reco-wrap{
  position: relative;
  border-radius: 18px;
  overflow: hidden;
  margin-top: 18px;
  margin-bottom: 16px;
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: 0 18px 44px rgba(0,0,0,0.45);
  transition: transform 180ms ease, box-shadow 180ms ease;
}
.reco-wrap:hover{
  transform: translateY(-2px);
  box-shadow: 0 24px 58px rgba(0,0,0,0.55);
}
.reco-wrap::before{
  content:"";
  position:absolute;
  inset:-120%;
  background: radial-gradient(900px 320px at 15% 20%, rgba(77,150,255,0.26), transparent 60%),
              radial-gradient(900px 340px at 85% 75%, rgba(0,210,168,0.18), transparent 60%),
              radial-gradient(900px 340px at 55% 70%, rgba(170,90,255,0.14), transparent 62%);
  animation: recoDrift 10.5s ease-in-out infinite;
}
@keyframes recoDrift{
  0%   { transform: translate(0,0); }
  50%  { transform: translate(34px,-18px); }
  100% { transform: translate(0,0); }
}
.reco-inner{
  position: relative;
  z-index: 2;
  padding: 18px 18px;
  background: rgba(0,0,0,0.28);
  backdrop-filter: blur(12px);
}
.reco-bar{
  position:absolute;
  left:0; top:0; bottom:0;
  width: 6px;
  background: linear-gradient(180deg, #4D96FF, #00D2A8, #AA5AFF);
  opacity: 0.95;
}
.reco-title{
  display:flex;
  align-items:center;
  gap:10px;
  font-size: 18px;
  font-weight: 950;
  color: rgba(255,255,255,0.95);
  margin-bottom: 8px;
}
.reco-pill{
  display:inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.2px;
  margin-right: 6px;
  background: rgba(77,150,255,0.16);
  border: 1px solid rgba(77,150,255,0.30);
  color: rgba(255,255,255,0.92);
}
.reco-text{
  font-size: 15px;
  line-height: 1.7;
  color: rgba(255,255,255,0.88);
}

/* ============================
   BUTTON HOVER COLOR ANIMATION
   ============================ */
.stButton > button{
  position: relative;
  border-radius: 12px !important;
  font-weight: 900 !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  background: rgba(255,255,255,0.06) !important;
  color: rgba(255,255,255,0.92) !important;
  overflow: hidden;
  transform: translateZ(0);
  transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease, background 180ms ease;
  box-shadow: 0 10px 26px rgba(0,0,0,0.25);
}
.stButton > button::before{
  content:"";
  position:absolute;
  inset:-120%;
  background: linear-gradient(
    90deg,
    rgba(77,150,255,0.00),
    rgba(77,150,255,0.55),
    rgba(0,210,168,0.55),
    rgba(170,90,255,0.55),
    rgba(77,150,255,0.00)
  );
  opacity: 0;
  filter: blur(10px);
  transform: rotate(8deg);
  transition: opacity 200ms ease;
}
.stButton > button::after{
  content:"";
  position:absolute;
  top:-60%;
  left:-40%;
  width: 80%;
  height: 220%;
  background: linear-gradient(120deg, rgba(255,255,255,0.0), rgba(255,255,255,0.16), rgba(255,255,255,0.0));
  transform: rotate(18deg);
  opacity: 0;
  transition: opacity 200ms ease;
}
.stButton > button:hover{
  transform: translateY(-2px) scale(1.01);
  box-shadow: 0 16px 36px rgba(0,0,0,0.35);
  border-color: rgba(77,150,255,0.38) !important;
  background: rgba(77,150,255,0.10) !important;
}
.stButton > button:hover::before{
  opacity: 1;
  animation: btnGlow 1.35s linear infinite;
}
.stButton > button:hover::after{
  opacity: 1;
  animation: btnShine 1.1s ease-in-out infinite;
}
.stButton > button:active{
  transform: translateY(0px) scale(0.99);
}
.stButton > button > div,
.stButton > button > span{
  position: relative;
  z-index: 2;
}
@keyframes btnGlow{
  0%   { transform: translateX(-8%) rotate(8deg); }
  100% { transform: translateX(8%) rotate(8deg); }
}
@keyframes btnShine{
  0%   { transform: translateX(-30%) rotate(18deg); }
  100% { transform: translateX(120%) rotate(18deg); }
}

/* ============================
   FOOTER (CENTERED)
   ============================ */
.footer{
  margin-top: 34px;
  padding: 18px 18px;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.10);
  background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
  box-shadow: 0 18px 44px rgba(0,0,0,0.45);
  overflow: hidden;
  position: relative;
  text-align: center;
}
.footer::before{
  content:"";
  position:absolute;
  inset:-120%;
  background: radial-gradient(900px 320px at 15% 20%, rgba(77,150,255,0.20), transparent 60%),
              radial-gradient(900px 340px at 85% 75%, rgba(0,210,168,0.14), transparent 60%),
              radial-gradient(900px 340px at 55% 70%, rgba(170,90,255,0.12), transparent 62%);
  animation: footerDrift 10.5s ease-in-out infinite;
  opacity: 0.9;
}
@keyframes footerDrift{
  0%   { transform: translate(0,0); }
  50%  { transform: translate(26px,-14px); }
  100% { transform: translate(0,0); }
}
.footer-content{
  position: relative;
  z-index: 2;
  display:flex;
  flex-direction: column;
  align-items:center;
  justify-content:center;
  gap: 12px;
}
.footer-avatar{
  width: 74px;
  height: 74px;
  border-radius: 18px;
  object-fit: cover;
  box-shadow: 0 14px 30px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.10) inset;
}
.footer-text{ line-height: 1.2; }
.footer-name{
  font-size: 18px;
  font-weight: 950;
  color: rgba(255,255,255,0.95);
}
.footer-tagline{
  font-size: 13px;
  margin-top: 6px;
  color: rgba(255,255,255,0.78);
}
</style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Load companies.xml
# -----------------------------
@st.cache_data
def load_companies_from_xml(xml_path: str = r"./Assets/companies.xml") -> dict:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    companies = {}
    for company in root.findall("company"):
        name = company.find("name").text.strip()
        ticker = company.find("ticker").text.strip()
        companies[name] = ticker
    return companies

companies = load_companies_from_xml()
options = [f"{name} ({ticker})" for name, ticker in companies.items()]

# -----------------------------
# Load Yahoo Finance Data
# -----------------------------
@st.cache_data
def load_data(ticker: str, start_dt, end_dt) -> pd.DataFrame:
    df = yf.download(
        ticker,
        start=start_dt,
        end=end_dt,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.reset_index()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df.reset_index(drop=True)

# -----------------------------
# Prophet / NeuralProphet helpers
# -----------------------------
def to_prophet_df(df_prices: pd.DataFrame) -> pd.DataFrame:
    df = df_prices[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"}).copy()
    df["ds"] = pd.to_datetime(df["ds"])
    return df.dropna()

def to_neuralprophet_df(df_prices: pd.DataFrame) -> pd.DataFrame:
    df = df_prices[["Date", "Close"]].rename(columns={"Date": "ds", "Close": "y"}).copy()
    df["ds"] = pd.to_datetime(df["ds"])
    return df.dropna()

def monthly_summary_from_yhat(forecast_future: pd.DataFrame, yhat_col: str) -> pd.DataFrame:
    out = forecast_future.copy()
    out["month"] = pd.to_datetime(out["ds"]).dt.month
    return out.groupby("month", as_index=False)[yhat_col].mean()

def find_yearly_col(df: pd.DataFrame):
    if "yearly" in df.columns:
        return "yearly"
    yearly_cols = [c for c in df.columns if "yearly" in c.lower()]
    return yearly_cols[0] if yearly_cols else None

# -----------------------------
# Session State Defaults
# -----------------------------
if "selected_company" not in st.session_state:
    st.session_state.selected_company = options[0] if options else None
if "start_date" not in st.session_state:
    st.session_state.start_date = date(2016, 1, 1)
if "end_date" not in st.session_state:
    st.session_state.end_date = date(2026, 1, 1)
if "forecast_years" not in st.session_state:
    st.session_state.forecast_years = 1

def clear_selection():
    st.session_state.selected_company = options[0] if options else None
    st.session_state.start_date = date(2016, 1, 1)
    st.session_state.end_date = date(2026, 1, 1)
    st.session_state.forecast_years = 1

# -----------------------------
# Header image (Assets/stock.jpg)
# -----------------------------
if "_stock_logo_b64" not in st.session_state:
    logo_path = "./Assets/stock.jpg"
    try:
        with open(logo_path, "rb") as f:
            st.session_state["_stock_logo_b64"] = base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        st.session_state["_stock_logo_b64"] = ""

st.markdown(
    f"""
<div class="hero-wrap">
  <div class="hero-orb orb1"></div>
  <div class="hero-orb orb2"></div>
  <div class="hero-orb orb3"></div>

  <div class="hero-content">
    <img class="hero-logo" src="data:image/jpg;base64,{st.session_state["_stock_logo_b64"]}" />
    <div class="hero-title">Stock Price Prediction</div>
    <div class="hero-subtitle">Intelligent forecasting with Prophet & NeuralProphet</div>
    <div class="hero-type">Select a company, choose dates, and generate forecasts instantly.</div>
    <div class="hero-line"></div>
  </div>
</div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Inputs (subtitles removed)
# -----------------------------
st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)

_, center_col, _ = st.columns([1.2, 2.2, 1.2])
with center_col:
    st.markdown(
        """
        <div class="ui-card">
          <div class="ui-card-content">
            <div class="ui-label">🏢 Select Stock Company</div>
        """,
        unsafe_allow_html=True,
    )
    selected = st.selectbox("", options, key="selected_company", label_visibility="collapsed")
    st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown(
        """
        <div class="ui-card">
          <div class="ui-card-content">
            <div class="ui-label">📅 Start Date</div>
        """,
        unsafe_allow_html=True,
    )
    st.date_input("", key="start_date", min_value=date(2000, 1, 1), label_visibility="collapsed")
    st.markdown("</div></div>", unsafe_allow_html=True)

with c2:
    st.markdown(
        """
        <div class="ui-card">
          <div class="ui-card-content">
            <div class="ui-label">🗓️ End Date</div>
        """,
        unsafe_allow_html=True,
    )
    st.date_input("", key="end_date", min_value=st.session_state.start_date, label_visibility="collapsed")
    st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)

_, center_col2, _ = st.columns([1.2, 2.2, 1.2])
with center_col2:
    st.markdown(
        """
        <div class="ui-card">
          <div class="ui-card-content">
            <div class="ui-label">⏳ Forecast Period</div>
        """,
        unsafe_allow_html=True,
    )
    st.slider("", 1, 10, key="forecast_years", label_visibility="collapsed")
    st.markdown("</div></div>", unsafe_allow_html=True)

# Recommendation
st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
st.markdown(
    """
<div class="reco-wrap">
  <div class="reco-bar"></div>
  <div class="reco-inner">
    <div class="reco-title">✨ Recommendation</div>
    <div class="reco-text">
      <span class="reco-pill">Best Choice</span>
      <strong>Predict with Prophet</strong> is recommended for most users because it typically delivers
      <strong>stable</strong>, <strong>interpretable</strong>, and <strong>consistent</strong> forecasts.
      <br><br>
      <span class="reco-pill">Compare</span>
      Use <strong>NeuralProphet</strong> for experimentation and comparison, but for dependable results,
      <strong>Prophet is the best starting point</strong>.
    </div>
  </div>
</div>
    """,
    unsafe_allow_html=True,
)

# Buttons (3 columns)
st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
b1, b2, b3 = st.columns(3, gap="large")
with b1:
    prophet_clicked = st.button("🔮 Predict with Prophet", use_container_width=True)
with b2:
    neural_clicked = st.button("🤖 Predict with Neural Prophet", use_container_width=True)
with b3:
    st.button("🧹 Clear Selection", use_container_width=True, on_click=clear_selection)

# -----------------------------
# Convenience Variables
# -----------------------------
selected_name, selected_ticker = None, None
n_days = int(st.session_state.forecast_years) * 365
if selected:
    selected_name = selected.split(" (")[0]
    selected_ticker = companies[selected_name]

# -----------------------------
# Shared: load & show raw data
# -----------------------------
def show_raw_data(ticker: str):
    data = load_data(ticker, st.session_state.start_date, st.session_state.end_date)
    st.markdown("<div class='spacer-md'></div>", unsafe_allow_html=True)
    st.subheader("📥 Raw Stock Data")
    st.write(
        f"Data from {st.session_state.start_date} to {st.session_state.end_date} "
        f"({len(data)} rows)"
    )
    if data.empty:
        st.error("No data available for the selected range.")
        st.stop()
    st.dataframe(data, use_container_width=True, hide_index=True)
    return data

# ============================================================
# Prophet Forecasting & Plots (Weekly plot removed)
# ============================================================
if prophet_clicked:
    st.success(
        f"Running **Prophet** forecast for **{selected_name}** ({selected_ticker}) "
        f"for **{st.session_state.forecast_years} year(s)** (≈ {n_days} days)."
    )

    data = show_raw_data(selected_ticker)
    df_p = to_prophet_df(data)

    if len(df_p) < 2:
        st.error("Not enough valid data points to train the Prophet model.")
        st.stop()

    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(df_p)

    future = model.make_future_dataframe(periods=n_days, freq="D")
    forecast = model.predict(future)

    last_hist = df_p["ds"].max()
    forecast_future = forecast[forecast["ds"] > last_hist].copy()

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    st.subheader("📊 Forecasting Data Table (Prophet)")
    st.dataframe(
        forecast_future[["ds", "yhat", "yhat_lower", "yhat_upper"]].reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    st.subheader("📈 Actual vs Forecast (Prophet)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_p["ds"], y=df_p["y"], mode="lines", name="Actual",
                             line=dict(color="#FF6B6B", width=2)))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], mode="lines", name="Forecast",
                             line=dict(color="#4D96FF", width=2)))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"], mode="lines",
                             line=dict(width=0), showlegend=False))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"], mode="lines",
                             fill="tonexty", fillcolor="rgba(77,150,255,0.30)",
                             line=dict(width=0), name="Confidence Interval"))
    fig.update_layout(
        title=f"{selected_name} ({selected_ticker}) — Actual vs Forecast",
        xaxis_title="Date", yaxis_title="Adjusted Close (USD)",
        template="plotly_dark", hovermode="x unified",
        margin=dict(l=30, r=30, t=60, b=30),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    st.subheader("📉 Trend (Prophet)")
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=forecast["ds"], y=forecast["trend"], mode="lines", name="Trend",
                                   line=dict(color="#00D2A8", width=2)))
    fig_trend.update_layout(
        title=f"{selected_name} — Trend Component",
        xaxis_title="Date", yaxis_title="Trend",
        template="plotly_dark", hovermode="x unified",
        margin=dict(l=30, r=30, t=60, b=30),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    st.subheader("🗓️ Yearly Seasonality (Prophet)")
    yearly_col = find_yearly_col(forecast)
    if yearly_col:
        fig_yearly = go.Figure()
        fig_yearly.add_trace(go.Scatter(x=forecast["ds"], y=forecast[yearly_col], mode="lines", name="Yearly",
                                        line=dict(color="#4D96FF", width=2)))
        fig_yearly.update_layout(
            title=f"{selected_name} — Yearly Seasonality",
            xaxis_title="Date", yaxis_title="Seasonality Effect",
            template="plotly_dark", hovermode="x unified",
            margin=dict(l=30, r=30, t=60, b=30),
        )
        st.plotly_chart(fig_yearly, use_container_width=True)
    else:
        st.info("Yearly seasonality is not available in this forecast output.")

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    st.subheader("📅 Monthly Component (Prophet)")
    mdf = monthly_summary_from_yhat(forecast_future, "yhat")
    fig_month = go.Figure()
    fig_month.add_trace(go.Scatter(x=mdf["month"], y=mdf["yhat"], mode="lines+markers", name="Avg Forecast",
                                   line=dict(color="#00D2A8", width=2), marker=dict(size=8)))
    fig_month.update_layout(
        title=f"{selected_name} — Monthly Component (Avg Forecasted Price)",
        xaxis_title="Month", yaxis_title="Average Forecasted Price",
        xaxis=dict(dtick=1), template="plotly_dark",
        margin=dict(l=30, r=30, t=60, b=30),
    )
    st.plotly_chart(fig_month, use_container_width=True)

# ============================================================
# NeuralProphet Forecasting & Plots (Weekly plot removed)
# ============================================================
if neural_clicked:
    st.success(
        f"Running **NeuralProphet** forecast for **{selected_name}** ({selected_ticker}) "
        f"for **{st.session_state.forecast_years} year(s)** (≈ {n_days} days)."
    )

    data = show_raw_data(selected_ticker)
    df_np = to_neuralprophet_df(data)

    if len(df_np) < 2:
        st.error("Not enough valid data points to train the NeuralProphet model.")
        st.stop()

    np_model = NeuralProphet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False, epochs=50)
    np_model.fit(df_np, freq="D")

    future_np = np_model.make_future_dataframe(df_np, periods=n_days, n_historic_predictions=True)
    fc_np = np_model.predict(future_np)

    yhat_col = "yhat1" if "yhat1" in fc_np.columns else None
    if yhat_col is None:
        yhat_candidates = [c for c in fc_np.columns if c.lower().startswith("yhat")]
        if not yhat_candidates:
            st.error("NeuralProphet forecast does not contain a yhat column (e.g., yhat1).")
            st.stop()
        yhat_col = yhat_candidates[0]

    lower_col = f"{yhat_col}_lower" if f"{yhat_col}_lower" in fc_np.columns else None
    upper_col = f"{yhat_col}_upper" if f"{yhat_col}_upper" in fc_np.columns else None

    last_hist = df_np["ds"].max()
    fc_np_future = fc_np[fc_np["ds"] > last_hist].copy()

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    st.subheader("📊 Forecasting Data Table (NeuralProphet)")
    cols = ["ds", yhat_col]
    if lower_col and upper_col:
        cols += [lower_col, upper_col]
    st.dataframe(fc_np_future[cols].reset_index(drop=True), use_container_width=True, hide_index=True)

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    st.subheader("📈 Actual vs Forecast (NeuralProphet)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_np["ds"], y=df_np["y"], mode="lines", name="Actual",
                             line=dict(color="#FF6B6B", width=2)))
    fig.add_trace(go.Scatter(x=fc_np["ds"], y=fc_np[yhat_col], mode="lines", name="Forecast",
                             line=dict(color="#4D96FF", width=2)))
    if lower_col and upper_col:
        fig.add_trace(go.Scatter(x=fc_np["ds"], y=fc_np[upper_col], mode="lines", line=dict(width=0), showlegend=False))
        fig.add_trace(go.Scatter(x=fc_np["ds"], y=fc_np[lower_col], mode="lines",
                                 fill="tonexty", fillcolor="rgba(77,150,255,0.30)",
                                 line=dict(width=0), name="Confidence Interval"))
    fig.update_layout(
        title=f"{selected_name} ({selected_ticker}) — Actual vs Forecast",
        xaxis_title="Date", yaxis_title="Adjusted Close (USD)",
        template="plotly_dark", hovermode="x unified",
        margin=dict(l=30, r=30, t=60, b=30),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    st.subheader("📉 Trend (NeuralProphet)")
    if "trend" in fc_np.columns:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=fc_np["ds"], y=fc_np["trend"], mode="lines", name="Trend",
                                       line=dict(color="#00D2A8", width=2)))
        fig_trend.update_layout(
            title=f"{selected_name} — Trend Component",
            xaxis_title="Date", yaxis_title="Trend",
            template="plotly_dark", hovermode="x unified",
            margin=dict(l=30, r=30, t=60, b=30),
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Trend component is not available in this NeuralProphet forecast output.")

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    st.subheader("🗓️ Yearly Seasonality (NeuralProphet)")
    yearly_col = find_yearly_col(fc_np)
    if yearly_col:
        fig_yearly = go.Figure()
        fig_yearly.add_trace(go.Scatter(x=fc_np["ds"], y=fc_np[yearly_col], mode="lines", name="Yearly",
                                        line=dict(color="#4D96FF", width=2)))
        fig_yearly.update_layout(
            title=f"{selected_name} — Yearly Seasonality",
            xaxis_title="Date", yaxis_title="Seasonality Effect",
            template="plotly_dark", hovermode="x unified",
            margin=dict(l=30, r=30, t=60, b=30),
        )
        st.plotly_chart(fig_yearly, use_container_width=True)
    else:
        st.info("Yearly seasonality is not available in this forecast output.")

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    st.subheader("📅 Monthly Component (NeuralProphet)")
    mdf = monthly_summary_from_yhat(fc_np_future, yhat_col)
    fig_month = go.Figure()
    fig_month.add_trace(go.Scatter(x=mdf["month"], y=mdf[yhat_col], mode="lines+markers", name="Avg Forecast",
                                   line=dict(color="#00D2A8", width=2), marker=dict(size=8)))
    fig_month.update_layout(
        title=f"{selected_name} — Monthly Component (Avg Forecasted Price)",
        xaxis_title="Month", yaxis_title="Average Forecasted Price",
        xaxis=dict(dtick=1), template="plotly_dark",
        margin=dict(l=30, r=30, t=60, b=30),
    )
    st.plotly_chart(fig_month, use_container_width=True)

