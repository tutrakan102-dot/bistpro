import streamlit as st
import pandas as pd
import yfinance as yf
st.set_page_config(
    page_title="BIST Elite Panel",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>

html, body, [class*="css"] {
    font-size:16px;
}

.stDataFrame {
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="BIST 100 MOTOR v2", layout="wide")
st.title("BIST 100 MOTOR v2 - PROFESYONEL SİNYAL MOTORU")
st.markdown('<style>body {background-color:#f5f5f5;}</style>', unsafe_allow_html=True)

# BIST 100 hisseleri
hisseler = [
"AEFES.IS","AGHOL.IS","AHGAZ.IS","AKBNK.IS","AKSA.IS","AKSEN.IS",
"ALARK.IS","ARCLK.IS","ASELS.IS","ASTOR.IS","BIMAS.IS","BRSAN.IS",
"CCOLA.IS","CIMSA.IS","DOAS.IS","DOHOL.IS","ECILC.IS","EKGYO.IS",
"ENKAI.IS","EREGL.IS","FROTO.IS","GARAN.IS","GESAN.IS","GUBRF.IS",
"HEKTS.IS","ISCTR.IS","KCHOL.IS","KOZAL.IS","KRDMD.IS","MGROS.IS",
"ODAS.IS","OYAKC.IS","PETKM.IS","PGSUS.IS","SAHOL.IS","SASA.IS",
"SISE.IS","SMRTG.IS","TCELL.IS","THYAO.IS","TOASO.IS","TUPRS.IS",
"ULKER.IS","VAKBN.IS","VESTL.IS","YKBNK.IS"
]

# RSI hesaplama fonksiyonu
def rsi(data, period=14):
    delta = data.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# Aksiyon hesaplama fonksiyonu
def aksiyon_hesapla(rsi, puan, trend):
    if trend != "UP":
        return "🔴 Alma"
    if rsi >= 85:
        return "🔴 Geri çekilme bekle"
    elif rsi >= 75:
        return "🟠 Dikkatli al"
    elif rsi >= 65:
        return "🟡 Alınabilir"
    elif rsi >= 50:
        return "🟢 En iyi alım bölgesi"
    else:
        return "⚪ İzle"

# Sonuçları toplamak için liste
sonuclar = []
progress = st.progress(0)

for i, hisse in enumerate(hisseler):
    try:
        data = yf.download(hisse, period="6mo", progress=False)
        close = data["Close"]
        volume = data["Volume"]

        rsi_val = rsi(close)
        ma20 = close.rolling(20).mean()
        ma50 = close.rolling(50).mean()
        vol_avg = volume.rolling(20).mean()

        fiyat = close.iloc[-1].item()
        rsi_son = rsi_val.iloc[-1].item()
        rsi_onceki = rsi_val.iloc[-2].item()
        ma20_son = ma20.iloc[-1].item()
        ma50_son = ma50.iloc[-1].item()
        vol_son = volume.iloc[-1].item()
        vol_avg_son = vol_avg.iloc[-1].item()

        skor = 0

        # RSI puanı
        if rsi_son > 50:
            skor += (rsi_son - 50) * 1.5

        # Trend puanı
        if fiyat > ma20_son:
            skor += 15
        if ma20_son > ma50_son:
            skor += 15

        # Hacim puanı
        if vol_son > vol_avg_son:
            skor += 20

        # Yeni sinyal bonus
        if rsi_onceki < 50 and rsi_son > 50:
            skor += 25

        if skor > 0:
            sonuclar.append({
                "Hisse": hisse,
                "Puan": round(skor,1),
                "RSI": round(rsi_son,1),
                "Hacim Gücü": round(vol_son/vol_avg_son,2),
                "Trend": "UP" if ma20_son > ma50_son else "DOWN"
            })

    except:
        pass

    progress.progress((i+1)/len(hisseler))

# DataFrame oluşturma
df = pd.DataFrame(sonuclar)

# Aksiyon sütunu ekleme
df["Aksiyon"] = df.apply(
    lambda x: aksiyon_hesapla(x["RSI"], x["Puan"], x["Trend"]),
    axis=1
)
# Elite Liste: sadece En iyi alım bölgesi
st.divider()
elite_df = df[df["Aksiyon"] == "🟢 En iyi alım bölgesi"]
st.subheader("💎 ELITE LİSTE - En iyi alım bölgesi")
st.dataframe(elite_df, use_container_width=True)
if elite_df.empty:
    st.write("Bugün Elite Liste için uygun hisse yok.")
# Skora göre sıralama
df = df.sort_values("Puan", ascending=False)
df_guclu = df.head(5)
import os
from datetime import datetime

# Log dosyası adı
log_dosya = "sinyal_log.csv"

# Bugünün tarihi
bugun = datetime.today().strftime("%Y-%m-%d")

# Log DataFrame
log_df = df.copy()
log_df.insert(0, "Tarih", bugun)

# Eğer dosya varsa ekle, yoksa oluştur
if os.path.exists(log_dosya):
    log_df.to_csv(log_dosya, mode='a', index=False, header=False)
else:
    log_df.to_csv(log_dosya, index=False)

st.write(f"Sinyaller log dosyasına kaydedildi: {log_dosya}")
# Panelde gösterim
st.subheader("🔥 Tüm Sinyaller")
st.dataframe(df, use_container_width=True)

st.subheader("🔥 EN GÜÇLÜ 5")
st.dataframe(df_guclu, use_container_width=True)

st.write("Toplam sinyal:", len(df))