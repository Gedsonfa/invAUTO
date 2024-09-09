import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt 
import mplcyberpunk

tickers = ["^BVSP", "^GSPC", "BRL=X"]

dados_mercado = yf.download(tickers, period = "6mo")

dados_mercado = dados_mercado["Adj Close"]

dados_mercado = dados_mercado.dropna()

dados_mercado.columns = ["DOLAR", "IBOVESPA", "S&P500"]

print(dados_mercado)