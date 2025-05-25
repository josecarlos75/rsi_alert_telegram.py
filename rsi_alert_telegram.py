import yfinance as yf
import ta
import requests

TOKEN = '7656809858:AAEyaaYCgvmfXSFms8X8cwBYYI33qXch6F4'
CHAT_ID = 6213570196

def enviar_mensaje(texto):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': texto}
    resp = requests.post(url, data=payload)
    if resp.status_code == 200:
        print("Mensaje enviado correctamente a Telegram.")
    else:
        print(f"Error al enviar mensaje: {resp.text}")

def obtener_rsi(ticker="SOL-USD", periodos=14):
    data = yf.download(ticker, period="1mo", interval="1d", auto_adjust=True)
    # Convertir la columna Close a 1D usando squeeze()
    close_prices = data['Close'].squeeze()
    rsi = ta.momentum.RSIIndicator(close_prices, window=periodos).rsi()
    rsi_ultimo = rsi.iloc[-1]
    return rsi_ultimo

def main():
    rsi_actual = obtener_rsi()
    print(f'RSI actual de SOL-USD: {rsi_actual:.2f}')
    if rsi_actual <= 30:
        enviar_mensaje(f'RSI está en sobreventa: {rsi_actual:.2f}')
    else:
        print("RSI en zona neutra o sobrecompra. No se envía mensaje.")

if __name__ == "__main__":
    main()
