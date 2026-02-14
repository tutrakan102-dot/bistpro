import yfinance as yf
from ta.momentum import RSIIndicator

hisseler = [
    "ASELS.IS",
    "THYAO.IS",
    "KCHOL.IS",
    "BRSAN.IS"
]

print("\nRSI 50 ÜSTÜ HİSSELER:\n")

for hisse in hisseler:

    data = yf.download(hisse, period="3mo")

    if data.empty:
        continue

    close = data["Close"].squeeze()

    rsi = RSIIndicator(close).rsi()

    son_rsi = rsi.iloc[-1]

    if son_rsi > 50:
        print(f"{hisse} → RSI: {son_rsi:.2f}")