import requests

def buscar_vagas_brasil():
    """
    Consome a API do GitHub (backend-br/vagas) e filtra por perfil e modalidade remota.
    """
    url_api = "https://api.github.com/repos/backend-br/vagas/issues"
    filtros = {"state": "open", "per_page": 100}
    
    # Configurações do seu Funil
    perfil_vaga = ['estágio', 'estagio', 'trainee', 'júnior', 'junior', 'jr', 'python', 'django']
    modalidade = ['remoto', 'anywhere', 'home office', 'distância', 'remota']
    
    try:
        resposta = requests.get(url_api, params=filtros, timeout=10)
        resposta.raise_for_status()
        issues = resposta.json()
        
        vagas_limpas = []
        
        for issue in issues:
            # 1. Ignora Pull Requests
            if 'pull_request' in issue:
                continue
                
            # 2. Prepara os textos para busca (tudo em minúsculo)
            titulo_vaga = issue.get('title', '').lower()
            corpo_vaga = issue.get('body', '')
            corpo_vaga = corpo_vaga.lower() if corpo_vaga else ""
            texto_completo = titulo_vaga + " " + corpo_vaga
            
            # 3. Aplica a Lógica de Filtragem (Perfil AND Remoto)
            tem_perfil = any(termo in titulo_vaga for termo in perfil_vaga)
            eh_remota = any(termo in texto_completo for termo in modalidade)
            
            if tem_perfil and eh_remota:
                vagas_limpas.append({
                    'id': str(issue.get('number')),
                    'titulo': issue.get('title'),
                    'empresa': issue.get('user', {}).get('login', 'Recrutador'),
                    'link': issue.get('html_url'),
                    'data_publicacao': issue.get('created_at')
                })
            
            # Limite de 5 para não sobrecarregar o Telegram de uma vez
            if len(vagas_limpas) == 5:
                break
                
        return vagas_limpas
        
    except requests.exceptions.RequestException as erro:
        print(f"❌ Erro ao buscar vagas no GitHub: {erro}")
        return []

# Bloco de execução para testes manuais
if __name__ == "__main__":
    print("🔍 Buscando vagas compatíveis (Perfil + Remoto)...")
    vagas_encontradas = buscar_vagas_brasil()
    
    if vagas_encontradas:
        print(f"✅ {len(vagas_encontradas)} vagas encontradas!\n")
        for v in vagas_encontradas:
            print(f"- {v['titulo']} na {v['empresa']}")
    else:
        print("⚠️ Nenhuma vaga compatível encontrada no momento.")