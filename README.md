# 📈 Stock Market Prediction Web Application

### 🚀 **Live Demo**

🔗 [Try the Application Here](https://sam-stock-market-prediction.streamlit.app/) — **Harness the power of predictive analytics for smarter investing!**

---

## 📌 Project Overview

Make informed investment decisions with this powerful **Stock Market Prediction** app! Utilizing historical stock data and **Facebook Prophet**'s advanced time series forecasting, this application offers accurate, data-driven stock price predictions.

Built with **Streamlit** for a smooth and interactive user experience, it features dynamic visualizations and customizable forecasting horizons—perfect for traders, analysts, and enthusiasts.

---

## 🛠️ Tech Stack & Tools

| Technology              | Purpose                               |
| ----------------------- | ------------------------------------- |
| 🐍 Python 3.7+          | Core programming language             |
| 🚀 Streamlit            | Fast, interactive web UI              |
| 📈 Facebook Prophet     | Robust time-series forecasting        |
| 💹 Yfinance             | Fetches historical stock data         |
| 📊 Plotly               | Interactive charts and visualization  |
| 🎨 Seaborn & Matplotlib | Statistical and static plotting       |
| 🐼 Pandas & NumPy       | Data processing & numerical computing |

---

## ✨ Key Features

* 📥 **Live Stock Data**: Fetches historical data directly from Yahoo Finance via `yfinance`
* 📊 **Interactive Visualizations**: Explore detailed, interactive time-series charts
* 🔮 **Accurate Forecasting**: Predict stock prices with Facebook Prophet, capturing trends and seasonality
* 🎯 **Customizable Inputs**: Choose any stock ticker, date range, and forecast horizon
* 📉 **Component Analysis**: Visualize trend, weekly, and yearly seasonal components of the forecast
* 💾 **Data Export**: Download raw historical and forecasted data as CSV files
* 📱 **Responsive Design**: User-friendly interface accessible on all devices

---

## ⚙️ Setup Instructions (Local Development)

### 1. Clone the Repository

```bash
git clone https://github.com/Samarth-Kumar-Samal-Sam/Stock-Market-Prediction.git

cd Stock-Market-Prediction
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Environment

* **Windows:**

```bash
venv\Scripts\activate
```

* **Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

---

## 📁 Repository Structure

```plaintext
.
├── Assets/
│   └── stock.jpg              # Image used in the web app
|   └── companies.xml          # List of companies 
├── Notebooks/
│   ├── Analysis.ipynb         # Exploratory data analysis
│   └── Prediction.ipynb       # Prediction model development
├── .gitignore                 # Git ignore file
├── LICENSE                    # License file
├── README.md                  # Project documentation
├── app.py                     # Streamlit application
└── requirements.txt           # Python dependencies
```

---

## 🚀 Usage Instructions

1. Select a stock ticker symbol from the dropdown menu.
2. Define the date range for historical data analysis.
3. Set the forecast horizon in years (customizable).
4. Click **Predict** to generate forecasts and visualizations.
5. Analyze interactive charts showing actual vs. predicted prices.
6. Dive into detailed forecast components — trend, weekly and yearly seasonality.
7. Download raw and forecasted data for offline use.

---

## 👨‍💻 Contributing

Contributions are warmly welcome! Follow these steps:

1. Fork the repository

2. Create a feature branch:

   ```bash
   git checkout -b feature-name
   ```

3. Commit your improvements:

   ```bash
   git commit -m "Add feature description"
   ```

4. Push to your branch:

   ```bash
   git push origin feature-name
   ```

5. Submit a Pull Request 🚀

---

## 📜 License

This project is licensed under the **[MIT License](LICENSE)**.

---

## 👤 Author

**Samarth Kumar Samal**
🔗 [GitHub Profile](https://github.com/Samarth-Kumar-Samal-Sam)

---

## 🙏 Acknowledgements

Special thanks to these fantastic tools and libraries:

* [Facebook Prophet](https://facebook.github.io/prophet/docs/quick_start.html)
* [Streamlit](https://docs.streamlit.io/)
* [Yfinance](https://pypi.org/project/yfinance/)
* [Pandas](https://pandas.pydata.org/docs/)
* [Numpy](https://numpy.org/doc/stable/)
* [Plotly](https://plotly.com/python/)
* [Matplotlib](https://matplotlib.org/)
* [Seaborn](https://seaborn.pydata.org/)

---
