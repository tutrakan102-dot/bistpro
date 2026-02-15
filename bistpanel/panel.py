import streamlit as st
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator

st.set_page_config(page_title="BIST PRO PANEL", layout="centered")

st.title("BIST PRO KARAR PANELI")

hisseler = ["ASELS.IS","AKBNK.IS","YKBNK.IS","THYAO.IS"]


def analiz(hisse, interval):

    try:

        data = yf.download(hisse, period="3mo", interval=interval, progress=False)

        if data.empty:
            return "VERI YOK", 0

        close = data["Close"].squeeze()

        rsi = RSIIndicator(close).rsi().iloc[-1]

        if rsi > 60:
            return "AL", round(rsi,2)

        elif rsi > 50:
            return "IZLE", round(rsi,2)

        else:
            return "BEKLE", round(rsi,2)

    except Exception as e:

        return "VERI YOK", 0



for hisse in hisseler:

    st.subheader(hisse)

    gunluk, rsi_g = analiz(hisse,"1d")

    dort, rsi_4 = analiz(hisse,"1h")

    saat, rsi_s = analiz(hisse,"15m")


    fiyat_data = yf.download(hisse, period="1d", progress=False)

    if not fiyat_data.empty:

        fiyat = fiyat_data["Close"].iloc[-1]

        hedef = round(float(fiyat) * 1.08 ,2)

        stop = round(float(fiyat) * 0.95 ,2)

    else:

        hedef = 0
        stop = 0


    guc = round((rsi_g + rsi_4 + rsi_s) / 30 ,1)


    st.write("Gunluk:", gunluk, " RSI:", rsi_g)

    st.write("4 Saat:", dort, " RSI:", rsi_4)

    st.write("Saatlik:", saat, " RSI:", rsi_s)

    st.write("Hedef:", hedef)

    st.write("Stop:", stop)

    st.write("Guc:", guc,"/10")

    st.write("------------------------")