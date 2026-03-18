import os
from buscador_vagas import buscar_vagas_brasil
from notificador import enviar_alerta_telegram
from datetime import datetime

# Define o nome do nosso "banco de dados" em arquivo de texto
ARQUIVO_MEMORIA = "historico_vagas.txt"

def carregar_memoria():
    """Lê o arquivo de texto e retorna uma lista com os IDs das vagas já enviadas."""
    if not os.path.exists(ARQUIVO_MEMORIA):
        return []
    
    with open(ARQUIVO_MEMORIA, "r") as arquivo:
        # Lê as linhas, remove espaços em branco e retorna como uma lista
        return [linha.strip() for linha in arquivo.readlines()]

def salvar_na_memoria(id_vaga):
    """Adiciona um novo ID de vaga ao arquivo de texto."""
    with open(ARQUIVO_MEMORIA, "a") as arquivo:
        arquivo.write(f"{id_vaga}\n")

def executar_robo():
    print("🤖 Iniciando varredura de vagas Full Stack...")
    
    vagas = buscar_vagas_brasil()
    vagas_enviadas = carregar_memoria()
    novas_vagas_encontradas = 0
    
    for vaga in vagas:
        id_str = str(vaga['id'])
        
        # A Trava de Idempotência: Se o ID já foi enviado, pula para a próxima vaga
        if id_str in vagas_enviadas:
            continue
            
        # Se for nova, monta a mensagem amigável com formatação Markdown
        mensagem = (
            f"🚀 *Nova Vaga Encontrada!*\n\n"
            f"💼 *Título:* {vaga['titulo']}\n"
            f"🏢 *Empresa:* {vaga['empresa']}\n"
            f"📅 *Publicada em:* {vaga['data_publicacao'][:10]}\n\n"
            f"🔗 [Clique aqui para acessar a vaga]({vaga['link']})"
        )
        
        # Tenta enviar para o Telegram
        sucesso = enviar_alerta_telegram(mensagem)
        
        # Se o Telegram aceitou, salvamos na memória para não mandar de novo
        if sucesso:
            salvar_na_memoria(id_str)
            novas_vagas_encontradas += 1

    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if novas_vagas_encontradas == 0:
        # Agora o log vai te dizer EXATAMENTE a hora que ele tentou buscar
        print(f"[{agora}] 💤 Nenhuma vaga nova compatível. O robô voltará a dormir.")
    else:
        print(f"[{agora}] ✅ Varredura concluída. {novas_vagas_encontradas} novos alertas enviados.")

if __name__ == "__main__":
    executar_robo()