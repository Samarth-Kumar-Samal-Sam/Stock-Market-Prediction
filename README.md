# 📈 Stock Market Prediction Web Application

## 🚀 **Live Demo**

🔗 **Try the Application Here:**  
https://stock-market-prediction-sam.streamlit.app/

Make data-driven investment insights using time-series forecasting powered by **YFinance, Prophet, and NeuralProphet**.

---

## 📌 Project Overview

The **Stock Market Prediction Web Application** is an interactive forecasting platform that enables users to analyze historical stock prices and generate future price predictions using advanced time-series models.

The application fetches real-time historical data from **Yahoo Finance (YFinance)** and applies both **Facebook Prophet** and **NeuralProphet** models to capture trends, seasonality, and complex temporal dependencies. Built with **Streamlit**, the app delivers a clean, responsive, and user-friendly interface with interactive visualizations and customizable forecasting horizons.

This project is ideal for investors, analysts, data science students, and financial enthusiasts.

---

## 🛠️ Tech Stack & Tools

| Technology              | Purpose                                             |
|------------------------|-----------------------------------------------------|
| 🐍 Python 3.7+          | Core programming language                           |
| 🚀 Streamlit            | Interactive web application framework               |
| 📈 Prophet              | Time-series forecasting (trend & seasonality)       |
| 🧠 NeuralProphet        | Neural network-based time-series forecasting        |
| 💹 YFinance             | Fetches historical stock market data                |
| 📊 Plotly               | Interactive data visualization                      |
| 🎨 Seaborn & Matplotlib | Statistical and static visualizations               |
| 🐼 Pandas & NumPy       | Data manipulation and numerical computing           |

---

## ✨ Key Features

- 📥 **Live Market Data**  
  Fetches historical stock price data directly from Yahoo Finance using `yfinance`.

- 📊 **Interactive Visualizations**  
  Dynamic charts for historical prices, forecasts, and predictions.

- 🔮 **Dual Forecasting Models**  
  - **Prophet** for interpretable trend and seasonality modeling  
  - **NeuralProphet** for advanced pattern learning using neural networks  

- 🎯 **Customizable Inputs**  
  Select stock ticker symbols, historical date range, and forecast horizon.

- 📉 **Component Analysis**  
  Visualize forecast components including:
  - Trend  
  - Weekly seasonality  
  - Yearly seasonality  

- 💾 **Data Export**  
  Download historical data and forecasted results as CSV files.

- 📱 **Responsive Design**  
  Optimized for desktop, tablet, and mobile devices.

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
2. Choose the historical date range for analysis.
3. Set the forecast horizon (in years).
4. Select the forecasting model (Prophet or NeuralProphet).
5. Click Predict to generate forecasts.
6. Analyze interactive charts comparing actual vs predicted prices.
7. Explore forecast components such as trend and seasonality.
8. Download historical and forecasted data for offline analysis.

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

* [Prophet (Facebook Prophet)](https://facebook.github.io/prophet/docs/quick_start.html)
* [NeuralProphet](https://neuralprophet.com/)
* [Streamlit](https://docs.streamlit.io/)
* [yfinance](https://pypi.org/project/yfinance/)
* [Pandas](https://pandas.pydata.org/docs/)
* [NumPy](https://numpy.org/doc/stable/)
* [Plotly](https://plotly.com/python/)
* [Matplotlib](https://matplotlib.org/)
* [Seaborn](https://seaborn.pydata.org/)
---

