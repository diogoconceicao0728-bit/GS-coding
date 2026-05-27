import os
from dotenv import load_dotenv

load_dotenv()

from tools import (
    get_crypto_price,
    calculate_trade_risk,
    save_trade_note,
    list_trade_notes,
    send_telegram_message,
    get_crypto_news,
)


def build_agent():
    from agno.agent import Agent
    from agno.db.sqlite import SqliteDb

    provider = os.getenv("AI_PROVIDER", "gemini").lower().strip()
    db_path = os.getenv("DATABASE_PATH", "data/tradesignal.db")

    if provider == "ollama":
        from agno.models.ollama import Ollama
        model = Ollama(id=os.getenv("OLLAMA_MODEL", "llama3.2"), host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    else:
        from agno.models.google import Gemini
        model = Gemini(id=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"), api_key=os.getenv("GOOGLE_API_KEY"))

    return Agent(
        name="TradeSignal Copilot",
        model=model,
        db=SqliteDb(db_file=db_path),
        tools=[
            get_crypto_price,
            calculate_trade_risk,
            save_trade_note,
            list_trade_notes,
            send_telegram_message,
            get_crypto_news,
        ],
        instructions=[
            "Você é um agente de apoio para day trade e notícias cripto.",
            "Use as tools quando precisar consultar preço, notícias, calcular risco, salvar diário ou enviar Telegram.",
            "Não prometa lucro e não trate nada como recomendação financeira garantida.",
            "Seja direto, prático e responda em português brasileiro.",
            "Sempre que falar de trade, destaque risco, stop e gerenciamento.",
        ],
        markdown=True,
        add_history_to_context=True,
    )
