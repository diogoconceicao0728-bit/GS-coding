# TradeSignal Copilot

Projeto desenvolvido para a **GS Coding for Security — 2º Semestre**.

O **TradeSignal Copilot** é um agente em Python com Agno voltado para apoio operacional em day trade cripto. A ideia não é prever mercado nem prometer resultado, mas reunir automações úteis em um fluxo simples: consultar preço, buscar notícias, calcular risco, registrar operações e enviar alertas no Telegram.

> Projeto educacional. Não é recomendação financeira.

---

## Objetivo do projeto

Criar um agente funcional com Python e Agno, utilizando tools próprias para executar ações reais ligadas ao universo de tecnologia, automação e mercado cripto.

O projeto atende aos principais pontos solicitados na avaliação:

- uso do framework Agno;
- integração com modelo de IA;
- criação de tools próprias;
- execução via terminal;
- uso de variáveis de ambiente;
- persistência local;
- organização de projeto;
- interface web simples com Flask;
- estrutura preparada para Docker.

---

## Tema escolhido

O tema escolhido foi um **assistente operacional para day trade cripto**.

A escolha do tema permite aplicar conceitos de automação, consumo de API, persistência local, integração com mensageria e uso de agente de IA em um cenário prático.

O agente pode ser usado para:

- consultar informações de mercado;
- calcular risco de uma operação;
- registrar anotações de trade;
- listar histórico operacional;
- buscar notícias recentes;
- enviar alertas para Telegram.

---

## Funcionamento geral

A aplicação possui uma versão principal em **CLI**, executada pelo terminal.

O usuário envia comandos em linguagem natural e o sistema direciona a solicitação para a tool adequada. Quando necessário, o projeto também permite uso do agente com IA via Agno.

A interface web em Flask utiliza as mesmas tools do projeto em modo rápido, reduzindo a latência durante a demonstração.

---

## Tools próprias implementadas

O projeto possui **6 tools próprias**, todas com execução real.

### 1. `get_crypto_price(symbol)`

Consulta dados reais de preço na API pública da Binance.

Retorna informações como:

- preço atual;
- máxima em 24h;
- mínima em 24h;
- volume;
- variação percentual.

---

### 2. `calculate_trade_risk(account_balance, risk_percent, entry_price, stop_price)`

Calcula o risco de uma operação com base nos dados informados pelo usuário.

A tool retorna:

- valor máximo a arriscar;
- distância até o stop;
- tamanho aproximado da posição;
- valor nocional da operação.

Essa tool ajuda a reforçar uma prática importante em operações: controle de risco antes da entrada.

---

### 3. `save_trade_note(symbol, bias, entry, stop, target, notes)`

Registra uma anotação de trade em banco SQLite local.

A anotação pode conter:

- ativo;
- direção da operação;
- entrada;
- stop;
- alvo;
- observações.

---

### 4. `list_trade_notes(limit)`

Consulta o banco SQLite e lista as últimas anotações registradas.

Essa tool demonstra persistência local e permite manter um diário operacional simples.

---

### 5. `send_telegram_message(message)`

Envia uma mensagem real para o Telegram usando um bot criado pelo BotFather.

Essa tool demonstra automação externa e integração com serviço de mensageria.

---

### 6. `get_crypto_news(limit)`

Busca notícias recentes sobre cripto em uma fonte RSS pública.

Essa tool permite trazer contexto de mercado para o usuário sem depender de respostas fixas ou simuladas.

---

## Critérios atendidos

| Critério da prova | Como foi atendido |
|---|---|
| Agente utilizando Agno | Projeto possui integração com Agno em `agent_factory.py` e execução via `main.py` |
| Modelo de IA | Uso de Gemini configurado por variável de ambiente |
| Tools próprias | Foram implementadas 6 tools funcionais em `tools.py` |
| Tools reais, não simuladas | As tools consultam API, calculam dados, usam SQLite, RSS e Telegram |
| CLI obrigatório | Execução principal feita por `python main.py` |
| Sessão/persistência | Uso de `session_id` e armazenamento local em SQLite |
| `.env` | Configurações sensíveis ficam separadas do código |
| `requirements.txt` | Dependências do projeto organizadas |
| Organização do projeto | Separação entre agente, tools, interface web e configurações |
| Interface web | Implementada com Flask em `web.py` |
| Docker | Projeto possui `Dockerfile` e instruções de execução |
| README | Este arquivo descreve objetivo, estrutura e funcionamento do projeto |

---

## Estrutura do projeto

```text
tradesignal_agno_telegram/
├── main.py
├── web.py
├── agent_factory.py
├── tools.py
├── fast_router.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── README.md
├── templates/
│   └── index.html
├── data/
└── logs/