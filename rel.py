import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt 
import mplcyberpunk

# Define tickers
tickers = ["^BVSP", "^GSPC", "BRL=X"]

# Download market data
dados_mercado = yf.download(tickers, period="6mo")

# Get Adjusted Close prices and clean data
dados_mercado = dados_mercado["Adj Close"].dropna()

# Renomear as colunas de acordo com a ordem correta dos dados baixados
dados_mercado.columns = ["IBOVESPA", "S&P500", "DOLAR"]

# Normalizar os dados para comparar melhor
dados_normalizados = dados_mercado / dados_mercado.iloc[0]

# Set the cyberpunk style
plt.style.use("cyberpunk")

# Plot each market index separately
plt.plot(dados_normalizados["IBOVESPA"], label="IBOVESPA")
plt.plot(dados_normalizados["S&P500"], label="S&P500")
plt.plot(dados_normalizados["DOLAR"], label="DOLAR")

# Add title and legend
plt.title("IBOVESPA, DOLAR, S&P500 (Normalizados) - Últimos 6 meses")
plt.legend()

# Show the plot
plt.show()

#Salvar imagem
#plt.savefig()
