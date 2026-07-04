# 3. The "Capsule 1.0" Logic
def check_capsule_strategy(ticker):
    try:
        data = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        # This prevents the MultiIndex error common in yfinance
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)

        # Calculate Indicators
        data['EMA_9'] = ta.ema(data['Close'], length=9)
        macd = ta.macd(data['Close'], fast=12, slow=26, signal=9)
        data['MACD'] = macd.iloc[:, 0]
        data['MACD_Signal'] = macd.iloc[:, 1]
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['CCI'] = ta.cci(data['High'], data['Low'], data['Close'], length=20)
        
        data = data.dropna()
        if data.empty: return "No Data"
        
        last = data.iloc[-1]
        
        # Capsule 1.0 Rules
        is_bullish = (last['Close'] > last['EMA_9']) and \
                     (last['MACD'] > last['MACD_Signal']) and \
                     (30 < last['RSI'] < 70) and \
                     (last['CCI'] > 100)
                     
        return "✅ BUY" if is_bullish else "❌ WATCH"
    except Exception as e:
        return f"Error: {e}"
