import requests

def buscar_vagas_brasil():
    """
    Função responsável por consumir a API pública da Remotive.
    Filtra vagas focadas em desenvolvimento de software com a palavra-chave 'Python' ou 'Django'.
    Retorna uma lista de dicionários contendo os dados limpos das vagas.
    """
    # Endpoint da API pública. Usamos query strings (?categoria e search) para o servidor
    # deles já fazer o trabalho pesado de filtrar, poupando a nossa memória e CPU.
    url_api = "https://api.github.com/repos/backend-br/vagas/issues"
    
    # Parâmetros: traz as 30 vagas abertas mais recentes
    filtros = {"state": "open", "per_page": 100}
    
    # O SEU NOVO FUNIL: Focado na sua realidade de mercado
    palavras_chave = [
        'estágio', 'estagio', 'trainee', 
        'júnior', 'junior', 'jr', 
        'python', 'django', 'flask', 'fastapi',
        'full stack', 'fullstack', 'full-stack',
        'backend', 'back-end'
    ]
    
    try:
        # A requisição GET agora vai para o GitHub
        resposta = requests.get(url_api, params=filtros, timeout=10)
        resposta.raise_for_status()
        issues = resposta.json()
        
        vagas_limpas = []
        
        for issue in issues:
            # Proteção: O GitHub mistura Pull Requests com Issues na mesma API. Pulamos os PRs.
            if 'pull_request' in issue:
                continue
                
            # Captura o título e joga para minúsculo para a checagem
            titulo_vaga = issue.get('title', '').lower()
            
            # Trava Lógica: Se achar estágio, júnior ou a sua stack no título, ele captura
            if any(termo in titulo_vaga for termo in palavras_chave):
                vagas_limpas.append({
                    'id': str(issue.get('number')), # O ID agora é o número da Issue no GitHub
                    'titulo': issue.get('title'),
                    'empresa': issue.get('user', {}).get('login', 'Recrutador'), # Quem postou a vaga
                    'link': issue.get('html_url'),
                    'data_publicacao': issue.get('created_at')
                })
                
            if len(vagas_limpas) == 5:
                break
                
        return vagas_limpas
        
    except requests.exceptions.RequestException as erro:
        print(f"❌ Erro ao buscar vagas no GitHub: {erro}")
        return []

# Bloco de teste isolado
if __name__ == "__main__":
    vagas = buscar_vagas_brasil()
    if vagas:
        for v in vagas:
            print(f"- {v['titulo']}")
    else:
        print("Nenhuma vaga correspondente encontrada nesta página.")

# Bloco de execução isolada para testarmos se o motor de busca está funcionando
if __name__ == "__main__":
    print("🔍 Buscando vagas remotas de Python...")
    vagas_encontradas = buscar_vagas_brasil()
    
    if vagas_encontradas:
        print(f"✅ {len(vagas_encontradas)} vagas processadas com sucesso!\n")
        for v in vagas_encontradas:
            print(f"- {v['titulo']} na {v['empresa']}")
    else:
        print("⚠️ Nenhuma vaga encontrada ou erro na requisição.")