import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt 
import mplcyberpunk
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv 
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurações de credenciais
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def obter_credenciais():
    """Obtém credenciais válidas do usuário, criando e salvando token se necessário."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Define tickers
tickers = ["^BVSP", "^GSPC", "BRL=X"]

# Download market data
dados_mercado = yf.download(tickers, period="6mo")

# Get Adjusted Close prices and clean data
dados_mercado = dados_mercado["Adj Close"].dropna()

# Renomear as colunas de acordo com a ordem correta dos dados baixados
dados_mercado.columns = ["IBOVESPA", "S&P500", "DOLAR"]

# Set the cyberpunk style
plt.style.use("cyberpunk")

# Salvar gráficos
plt.plot(dados_mercado["IBOVESPA"])
plt.title("IBOVESPA")
plt.savefig("/home/gedson/Downloads/ibovespa.png")
plt.close()

plt.plot(dados_mercado["DOLAR"])
plt.title("DOLAR")
plt.savefig("/home/gedson/Downloads/dolar.png")
plt.close()

plt.plot(dados_mercado["S&P500"])
plt.title("S&P500")
plt.savefig("/home/gedson/Downloads/sp500.png")
plt.close()

retornos_diarios = dados_mercado.pct_change()

retorno_ibovespa = str(round(retornos_diarios["IBOVESPA"].iloc[-1] * 100, 2)) + "%"
retorno_dolar = str(round(retornos_diarios["DOLAR"].iloc[-1] * 100, 2)) + "%"
retorno_sp = str(round(retornos_diarios["S&P500"].iloc[-1] * 100, 2)) + "%"

print("ibovespa: " + retorno_ibovespa)
print("dolar: " + retorno_dolar)
print("sp: " + retorno_sp)

def enviar_email():
    """Envia um e-mail com o relatório de mercado usando a API do Gmail."""
    creds = obter_credenciais()
    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # Criando o e-mail
        email = MIMEMultipart()
        email['From'] = os.getenv('EMAIL_USER')  # Substitua pelo seu e-mail
        email['To'] = os.getenv('EMAIL_DESTINATARIO')
        email['Subject'] = 'Relatório de Mercado'
        
        # Corpo do e-mail
        corpo_email = f'''Prezado diretor, segue o relatório de mercado:

        * O Ibovespa teve o retorno de {retorno_ibovespa}.
        * O Dólar teve o retorno de {retorno_dolar}.
        * O S&P500 teve o retorno de {retorno_sp}.

        Segue em anexo a performance dos ativos nos últimos 6 meses.

        Att,
        Melhor estagiário do mundo
        '''
        
        email.attach(MIMEText(corpo_email, 'plain'))
        
        # Anexando arquivos
        def anexar_arquivo(caminho_arquivo):
            with open(caminho_arquivo, 'rb') as arquivo:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(arquivo.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(caminho_arquivo)}')
                email.attach(part)

        # Anexar os três arquivos
        anexar_arquivo("/home/gedson/Downloads/ibovespa.png")
        anexar_arquivo("/home/gedson/Downloads/dolar.png")
        anexar_arquivo("/home/gedson/Downloads/sp500.png")

        raw_message = base64.urlsafe_b64encode(email.as_bytes()).decode()
        message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f'Sent message to {email["To"]} Message Id: {message["id"]}')
        
    except HttpError as error:
        print(f'An error occurred: {error}')

# Enviar o e-mail
enviar_email()
