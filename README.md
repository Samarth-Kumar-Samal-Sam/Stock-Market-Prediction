# Stock Prediction using Time Series, Prophet, Streamlit, and Yfinance

## Overview

Empower your investment decisions with **Stock Prediction**, a cutting-edge web application that leverages historical stock data and advanced time series forecasting. Using **Facebook Prophet** for robust trend and seasonality analysis, combined with **Streamlit** for an intuitive user interface and **Yfinance** to fetch live financial data, this project delivers reliable stock price forecasts with rich, interactive visualizations.

## Live Application

Try the app now: [Stock Prediction App](https://sam-stock-prediction-app.streamlit.app/)

---

## Features

- Fetches and visualizes historical stock prices from Yahoo Finance using `yfinance`.
- Uses Facebook Prophet to model and forecast stock prices, capturing trends and seasonality.
- Interactive, user-friendly interface built with Streamlit to select stocks, date ranges, and forecast horizons.
- Dynamic, interactive charts using Plotly for intuitive exploration of historical and forecasted stock prices.
- Detailed forecast components visualization including trends and yearly seasonality.
- Option to download raw and forecast data as CSV for further analysis.

---

## Technologies and Tools Used

- **Python 3.7+**  
- **Streamlit** – for rapid development of the web app interface  
- **Facebook Prophet** – for advanced time series forecasting  
- **Yfinance** – for downloading stock market data directly from Yahoo Finance  
- **Pandas & Numpy** – for data manipulation and processing  
- **Plotly** – for interactive plotting  
- **Matplotlib & Seaborn** – for detailed forecast components visualization  

---

## Installation and Setup Instructions

### Prerequisites

Make sure you have Python 3.7 or higher installed.

### Step-by-Step Guide

1. **Clone the repository**

   ```bash
   git clone https://github.com/Samarth-Kumar-Samal/Stock-Prediction-using-Prophet.git
   cd Stock-Prediction-using-Prophet
   ```

2. **Create a virtual environment**

   * On Windows:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   * On Linux/macOS:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   streamlit run app.py
   ```

5. **Open the app**

   Open your browser and go to the URL displayed in the terminal (default: [http://localhost:8501](http://localhost:8501)).

---

## Usage Instructions

* Select your preferred stock company from a comprehensive dropdown list.
* Choose the date range for historical data to analyze.
* Specify the forecast period in years.
* Click **Predict** to load the data, generate forecasts, and visualize results.
* Explore interactive charts comparing actual vs forecasted stock prices.
* View detailed forecast components such as trend and seasonality.
* Download the raw and forecasted datasets as CSV files for offline use.

---

## Contribution Guidelines

Contributions to improve this project are welcome!
Please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Commit your changes with a meaningful message:

   ```bash
   git commit -m "Add description of feature"
   ```

4. Push to your branch:

   ```bash
   git push origin feature/your-feature-name
   ```

5. Submit a pull request for review.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

**Samarth Kumar Samal**
GitHub: [https://github.com/Samarth-Kumar-Samal](https://github.com/Samarth-Kumar-Samal)

---

## Acknowledgements

Special thanks to the following libraries and resources that made this project possible:

* [Facebook Prophet](https://facebook.github.io/prophet/docs/quick_start.html)
* [Streamlit](https://docs.streamlit.io/)
* [Yfinance](https://pypi.org/project/yfinance/)
* [Pandas](https://pandas.pydata.org/docs/)
* [Numpy](https://numpy.org/doc/stable/)
* [Plotly](https://plotly.com/python/)
* [Matplotlib](https://matplotlib.org/)
* [Seaborn](https://seaborn.pydata.org/)

---

Thank you for exploring this project! Your feedback and contributions are greatly appreciated.
