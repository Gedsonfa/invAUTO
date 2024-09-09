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
#plt.show()

#Salvar imagem
#plt.savefig()

retornos_diarios = dados_mercado.pct_change()

#print(retornos_diarios)

retorno_ibovespa = retornos_diarios["IBOVESPA"].iloc[-1]

retorno_ibovespa = str(round(retorno_ibovespa * 100, 2)) + "%"

print("ibovespa: " + retorno_ibovespa)

retorno_dolar = retornos_diarios["DOLAR"].iloc[-1]

retorno_dolar = str(round(retorno_dolar * 100, 2)) + "%"

print("dolar: " + retorno_dolar)

retorno_sp = retornos_diarios["S&P500"].iloc[-1]

retorno_sp = str(round(retorno_sp * 100, 2)) + "%"

print("sp: " + retorno_sp)