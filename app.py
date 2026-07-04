def check_capsule_strategy(ticker):
    try:
        data = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        # Check if data actually loaded
        if data.empty:
            return "No data from YFinance"
            
        # Calculate Indicators
        data['EMA_9'] = ta.ema(data['Close'], length=9)
        # ... your other code ...
        return "Success"
        
    except Exception as e:
        # This will now print the REAL error on your screen
        return f"Error: {e}"
