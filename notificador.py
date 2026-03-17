import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (Token e Chat ID) para a memória do Python
load_dotenv()

def enviar_alerta_telegram(mensagem):
    """
    Função isolada responsável por disparar mensagens para o Telegram.
    Recebe uma string (mensagem) e retorna True se o envio foi bem-sucedido.
    """
    # Busca as credenciais de forma segura no sistema operacional
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        print("❌ Erro de Infraestrutura: Credenciais do Telegram não encontradas no arquivo .env")
        return False

    url_api = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # O Payload: o que estamos enviando para o servidor do Telegram
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "Markdown" # Tática: Permite usar negrito e links clicáveis na mensagem
    }

    try:
        # Executa o disparo HTTP POST
        resposta = requests.post(url_api, json=payload, timeout=10)
        
        # O método raise_for_status() força o erro se falhar
        resposta.raise_for_status() 
        
        # --- ADICIONE ESTA LINHA DE AUDITORIA AQUI ---
        print("🔍 RAW DATA do Telegram:", resposta.json())
        # ---------------------------------------------
        
        print("✅ Alerta enviado com sucesso para o Telegram!")
        return True
        
    except requests.exceptions.RequestException as erro:
        # Tratamento de falha: se a sua internet cair, o script não "quebra", apenas avisa.
        print(f"❌ Falha de comunicação com a API do Telegram: {erro}")
        return False

# Bloco de execução isolada: Este teste só roda se você executar ESTE arquivo diretamente.
# Se outro arquivo importar esta função, o teste abaixo é ignorado.
if __name__ == "__main__":
    mensagem_teste = "🚀 *Radar de Vagas operante!* Conexão estabelecida com sucesso."
    enviar_alerta_telegram(mensagem_teste)