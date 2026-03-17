# 📡 Radar de Vagas Automático (GitHub API + Telegram)

Este projeto é um microsserviço assíncrono projetado para varrer repositórios de vagas de tecnologia, filtrar oportunidades aderentes ao perfil (Estágio/Júnior em Python/Full Stack) e disparar alertas em tempo real via Telegram.

O objetivo arquitetural deste MVP é demonstrar consumo de APIs RESTful de terceiros, controle de estado local (idempotência) para evitar envios duplicados e automação a nível de sistema operacional.

## 🏗️ Arquitetura e Fluxo de Dados

1. **Extração de Dados (Data Source):** Consumo da API pública do GitHub, focado nas _Issues_ do repositório `backend-br/vagas` (maior mural de vagas de backend do Brasil). Aplicação de paginação para leitura em lote.
2. **Processamento e Filtragem:** Motor lógico implementado em Python que varre os títulos das _issues_ buscando palavras-chave específicas (ex: "python", "django", "estágio", "júnior"), normalizando os dados (Client-Side Filtering).
3. **Gestão de Estado (Idempotência):** Sistema de memória em arquivo texto (`historico_vagas.txt`). O ID (número da _issue_) de cada vaga enviada é registrado. Execuções futuras ignoram IDs já processados, garantindo que o usuário não receba notificações duplicadas.
4. **Notificação (Webhook):** Integração com a API de Bots do Telegram para envio de mensagens formatadas em Markdown contendo o título, empresa e link direto para a vaga.
5. **Automação de Infraestrutura:** Script projetado para rodar em _background_ via agendadores de tarefas nativos do sistema operacional (Cron no Linux / Task Scheduler no Windows).

## 🛠️ Stack Tecnológico

- **Linguagem:** Python 3.10+
- **Bibliotecas:** `requests` (HTTP clients), `python-dotenv` (Gestão de variáveis de ambiente)
- **Integrações:** GitHub API, Telegram Bot API

---

## ⚙️ Como Executar Localmente

### Pré-requisitos

- Python instalado na máquina.
- Um Bot do Telegram criado via [BotFather](https://t.me/botfather) (para obter o Token).
- O Chat ID do seu usuário ou grupo no Telegram.

### 1. Instalação e Configuração

# Clone o repositório

    ```bash
    git clone (https://github.com/Eirikr10/Buscador-de-Vagas-Github-Backend-BR.git)
    cd Buscador-de-Vagas-Github

    # Crie e ative o ambiente virtual
    python3 -m venv venv
    # No Linux/Mac:
    source venv/bin/activate
    # No Windows:
    venv\Scripts\activate

    # Instale as dependências
    pip install -r requirements.txt

### 2. Credenciais de Segurança

# Crie um Arquivo .env na raiz do projeto e insira as suas chaves da API do Telegram.

    TELEGRAM_TOKEN=seu_token_aqui
    TELEGRAM_CHAT_ID=seu_chat_id_aqui

### 3. Teste Manual:

# Rode o arquivo principal manualmente:

    python main.py

### 🤖 Automação de Execução (Background)

Para que o robô funcione como um radar autônomo, ele deve ser agendado no sistema operacional.

### 🐧 Para Sistemas Linux (Zorin OS, Ubuntu, etc.) via Cron:

### 1. Abra o terminal e edite o seu crontab:

    crontab -e

### 2. Adicione a linha abaixo para executar o robô a cada 4 horas( substitua /caminho/absoluto/ pelo caminho real da sua pasta ):

    0 */4 * * * cd /caminho/absoluto/radar_vagas && /caminho/absoluto/radar_vagas/venv/bin/python main.py >> /caminho/absoluto/radar_vagas/automacao.log 2>&1

### 🪟 Para Sistemas Windows via Agendador de Tarefas (Task Scheduler)

Para evitar que uma janela preta do terminal (CMD) abra a cada execução, você deve criar um script executável e agendá-lo.

1. Na pasta do projeto, crie um arquivo chamado executar_robo.bat com o seguinte conteúdo(ajuste os caminhos):

    ```bat
    @echo off
    cd C:\caminho\absoluto\para\radar_vagas
    call venv\Scripts\activate
    python main.py
    ```

2. Abra o menu Iniciar do Windows, busque por Agendador de Tarefas (Task Scheduler) e clique em Criar Tarefa...(Create Task).

3. Na aba Geral, dê o nome "Radar de Vagas Python" e marque a opção "Executar estando o usuário logado ou não" (isso roda o script em modo silencioso/background).

4. Na aba Gatilhos (Triggers), crie um novo e defina para repetir a tarefa a cada 4 horas indefinidamente.

5. Na aba Ações (Actions), crie uma nova, selecione "Iniciar um programa" e aponte para o arquivo executar_robo.bat que você criou. Salve a tarefa.
