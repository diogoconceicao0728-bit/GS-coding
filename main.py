import os
from dotenv import load_dotenv
from agent_factory import build_agent

load_dotenv()


def main():
    session_id = os.getenv("AGENT_SESSION_ID", "tradesignal-session-001")
    agent = build_agent()

    print("=" * 60)
    print("TradeSignal Copilot - Agente IA com Agno")
    print("Digite sua pergunta ou 'sair' para encerrar.")
    print("Exemplos:")
    print("- Consulte o preço do BTCUSDT")
    print("- Busque 3 notícias recentes de cripto")
    print("- Calcule risco com banca 1000, risco 2%, entrada 65000 e stop 64000")
    print("- Salve uma anotação para ETHUSDT com viés comprado")
    print("- Envie para o Telegram um resumo do BTC")
    print("=" * 60)

    while True:
        pergunta = input("\nVocê: ").strip()
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o agente.")
            break
        if not pergunta:
            continue
        try:
            agent.print_response(pergunta, session_id=session_id, stream=True)
        except Exception as erro:
            print(f"Erro ao executar o agente: {erro}")


if __name__ == "__main__":
    main()
