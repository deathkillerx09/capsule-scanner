import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd

# 1. Setup the Web Page
st.set_page_config(page_title="Capsule 1.0 Scanner", layout="centered")
st.title("🚀 Capsule 1.0 Scanner")

# 2. Your Stock List
stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HINDUNILVR.NS", "SBIN.NS"]

# 3. The "Capsule 1.0" Logic
def check_capsule_strategy(ticker):
    try:
        # Download data
        data = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        # FIX: Ensure columns are flattened if they are MultiIndex
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        if data.empty: 
            return "No Data"

        # Calculate Indicators
        data['EMA_9'] = ta.ema(data['Close'], length=9)
        macd = ta.macd(data['Close'], fast=12, slow=26, signal=9)
        
        # Safely extract MACD
        if macd is not None:
            data['MACD'] = macd.iloc[:, 0]
            data['MACD_Signal'] = macd.iloc[:, 1]
            
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['CCI'] = ta.cci(data['High'], data['Low'], data['Close'], length=20)
        
        data = data.dropna()
        if data.empty: 
            return "No Data"
        
        last = data.iloc[-1]
        
        # Capsule 1.0 Rules
        is_bullish = (last['Close'] > last['EMA_9']) and \
                     (last['MACD'] > last['MACD_Signal']) and \
                     (30 < last['RSI'] < 70) and \
                     (last['CCI'] > 100)
                     
        return "✅ BUY" if is_bullish else "❌ WATCH"
    except Exception as e:
        return f"Error: {e}"

# 4. Create the Dashboard Table
st.write("Scanning your stocks for Capsule 1.0 setup...")

results = []
for ticker in stocks:
    status = check_capsule_strategy(ticker)
    results.append({"Ticker": ticker, "Status": status})

# Display the table
df = pd.DataFrame(results)
st.table(df)

# Button to refresh
if st.button('Refresh Data'):
    st.rerun()
