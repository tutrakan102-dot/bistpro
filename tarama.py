import yfinance as yf
from ta.momentum import RSIIndicator

# BIST hisse listesi (şimdilik örnek, sonra tamamını ekleyeceğiz)

hisseler = [

"ASELS.IS",
"THYAO.IS",
"KCHOL.IS",
"BRSAN.IS",
"EREGL.IS",
"SISE.IS",
"TUPRS.IS",
"AKBNK.IS",
"YKBNK.IS",
"ISCTR.IS"

]

sonuclar = []

print("\nTaranıyor...\n")

for hisse in hisseler:

    try:

        data = yf.download(hisse, period="3mo")

        close = data["Close"].squeeze()

        rsi = RSIIndicator(close).rsi().iloc[-1]

        if 55 < rsi < 65:

            sonuclar.append((hisse, round(rsi,2)))

    except:

        pass


# sırala

sonuclar.sort(key=lambda x: x[1], reverse=True)


print("\nRSI 50 ÜSTÜ HİSSELER:\n")

for s in sonuclar:

    print(s[0], "→ RSI:", s[1])