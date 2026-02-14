import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

# Kullanıcıdan hisse al
hisse = input("Hisse gir (örnek: ASELS.IS): ")

# Veri çek
data = yf.download(hisse, period="6mo")

# EMA
data["EMA20"] = EMAIndicator(data["Close"].squeeze(), window=20).ema_indicator()
data["EMA50"] = EMAIndicator(data["Close"].squeeze(), window=50).ema_indicator()

# RSI
data["RSI"] = RSIIndicator(data["Close"].squeeze()).rsi()

# Grafik
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
    row_heights=[0.7, 0.3]
)

fig.add_trace(
    go.Candlestick(
        x=data.index,
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        name="Fiyat"
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=data.index, y=data["EMA20"], name="EMA20"),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=data.index, y=data["EMA50"], name="EMA50"),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=data.index, y=data["RSI"], name="RSI"),
    row=2, col=1
)

fig.update_layout(
    title=hisse + " Grafik",
    xaxis_rangeslider_visible=False
)

fig.show()