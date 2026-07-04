def check_capsule_strategy(ticker, interval):
    try:
        # ... (same download logic as before) ...
        data = yf.download(ticker, period="2y", interval=interval, progress=False)
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
        
        # Calculate Indicators
        data['EMA_9'] = ta.ema(data['Close'], length=9)
        macd = ta.macd(data['Close'], fast=12, slow=26, signal=9)
        if macd is not None:
            data['MACD'] = macd.iloc[:, 0]
            data['MACD_Signal'] = macd.iloc[:, 1]
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['CCI'] = ta.cci(data['High'], data['Low'], data['Close'], length=20)
        data = data.dropna()
        
        last = data.iloc[-1]
        
        # --- ADD THIS DEBUG PRINT ---
        if ticker == "MANGLMCEM.NS":
            st.write(f"DEBUG {interval}: RSI={last['RSI']:.2f}, CCI={last['CCI']:.2f}, Close={last['Close']:.2f}")

        is_bullish = (last['Close'] > last['EMA_9']) and \
                     (last['MACD'] > last['MACD_Signal']) and \
                     (30 < last['RSI'] < 70) and \
                     (last['CCI'] > 100)
                     
        return "✅ BUY" if is_bullish else "❌ WATCH"
    except Exception as e:
        return f"Error: {e}"
