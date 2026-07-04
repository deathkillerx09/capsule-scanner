import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd

st.set_page_config(page_title="Capsule 1.0 Multi-Scanner", layout="wide")
st.title("🚀 Capsule 1.0 Multi-Timeframe Scanner")

stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HINDUNILVR.NS", "SBIN.NS"]

def check_capsule_strategy(ticker, interval):
    try:
        # Use a longer period to ensure we have enough data for Monthly/Weekly indicators
        period = "2y" if interval in ["1wk", "1mo"] else "6mo"
        data = yf.download(ticker, period=period, interval=interval, progress=False)
        
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        if data.empty: return "No Data"

        # Calculate Indicators
        data['EMA_9'] = ta.ema(data['Close'], length=9)
        macd = ta.macd(data['Close'], fast=12, slow=26, signal=9)
        if macd is not None:
            data['MACD'] = macd.iloc[:, 0]
            data['MACD_Signal'] = macd.iloc[:, 1]
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['CCI'] = ta.cci(data['High'], data['Low'], data['Close'], length=20)
        
        data = data.dropna()
        if data.empty: return "No Data"
        
        last = data.iloc[-1]
        
        is_bullish = (last['Close'] > last['EMA_9']) and \
                     (last['MACD'] > last['MACD_Signal']) and \
                     (30 < last['RSI'] < 70) and \
                     (last['CCI'] > 100)
                     
        return "✅ BUY" if is_bullish else "❌ WATCH"
    except Exception:
        return "⚠️ ERROR"

st.write("Scanning for setups across Daily, Weekly, and Monthly timeframes...")

# Generate Results
results = []
for ticker in stocks:
    results.append({
        "Ticker": ticker,
        "Daily": check_capsule_strategy(ticker, "1d"),
        "Weekly": check_capsule_strategy(ticker, "1wk"),
        "Monthly": check_capsule_strategy(ticker, "1mo")
    })

# Display the table
st.table(pd.DataFrame(results))

if st.button('Refresh Data'):
    st.rerun()
