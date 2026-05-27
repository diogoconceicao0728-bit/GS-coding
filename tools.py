"""Tools próprias do projeto TradeSignal Copilot.
Todas executam ações reais: API pública, cálculo, SQLite, Telegram e leitura RSS.
"""

import os
import sqlite3
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DATABASE_PATH", "data/tradesignal.db")


def _connect_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS trade_journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            symbol TEXT NOT NULL,
            bias TEXT NOT NULL,
            entry REAL,
            stop REAL,
            target REAL,
            notes TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            destination TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    return conn


def get_crypto_price(symbol: str = "BTCUSDT") -> str:
    """Consulta o preço atual e variação de 24h de um par cripto na API pública da Binance, sem chave de API."""
    symbol = symbol.upper().replace("/", "").strip()
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        response = requests.get(url, params={"symbol": symbol}, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = float(data["lastPrice"])
        change = float(data["priceChangePercent"])
        high = float(data["highPrice"])
        low = float(data["lowPrice"])
        volume = float(data["volume"])
        return (
            f"Par: {symbol}\n"
            f"Preço atual: {price:.6f}\n"
            f"Variação 24h: {change:.2f}%\n"
            f"Máxima 24h: {high:.6f}\n"
            f"Mínima 24h: {low:.6f}\n"
            f"Volume 24h: {volume:.2f}"
        )
    except Exception as erro:
        return f"Não foi possível consultar o preço de {symbol}. Erro: {erro}"


def calculate_trade_risk(account_balance: float, risk_percent: float, entry_price: float, stop_price: float) -> str:
    """Calcula risco financeiro e tamanho aproximado da posição com base em banca, percentual de risco, entrada e stop."""
    try:
        account_balance = float(account_balance)
        risk_percent = float(risk_percent)
        entry_price = float(entry_price)
        stop_price = float(stop_price)
        risk_money = account_balance * (risk_percent / 100)
        distance = abs(entry_price - stop_price)
        if distance == 0:
            return "Entrada e stop não podem ser iguais."
        quantity = risk_money / distance
        notional = quantity * entry_price
        return (
            f"Banca: {account_balance:.2f}\n"
            f"Risco configurado: {risk_percent:.2f}%\n"
            f"Valor em risco: {risk_money:.2f}\n"
            f"Entrada: {entry_price:.4f}\n"
            f"Stop: {stop_price:.4f}\n"
            f"Distância até o stop: {distance:.4f}\n"
            f"Quantidade aproximada: {quantity:.6f}\n"
            f"Valor nocional aproximado: {notional:.2f}\n"
            "Observação: cálculo educacional, não é recomendação de investimento."
        )
    except Exception as erro:
        return f"Erro ao calcular risco: {erro}"


def save_trade_note(symbol: str, bias: str, entry: Optional[float] = None, stop: Optional[float] = None, target: Optional[float] = None, notes: str = "") -> str:
    """Salva uma anotação de trade em SQLite para criar histórico local de decisões e estudos."""
    try:
        conn = _connect_db()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "INSERT INTO trade_journal (created_at, symbol, bias, entry, stop, target, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (created_at, symbol.upper(), bias, entry, stop, target, notes),
        )
        conn.commit()
        conn.close()
        return f"Anotação salva para {symbol.upper()} em {created_at}."
    except Exception as erro:
        return f"Erro ao salvar anotação: {erro}"


def list_trade_notes(limit: int = 5) -> str:
    """Lista as últimas anotações salvas no diário de trades em SQLite."""
    try:
        conn = _connect_db()
        cursor = conn.execute(
            "SELECT id, created_at, symbol, bias, entry, stop, target, notes FROM trade_journal ORDER BY id DESC LIMIT ?",
            (int(limit),),
        )
        rows = cursor.fetchall()
        conn.close()
        if not rows:
            return "Nenhuma anotação encontrada no diário."
        linhas = []
        for row in rows:
            linhas.append(
                f"#{row[0]} | {row[1]} | {row[2]} | viés: {row[3]} | entrada: {row[4]} | stop: {row[5]} | alvo: {row[6]} | notas: {row[7]}"
            )
        return "\n".join(linhas)
    except Exception as erro:
        return f"Erro ao listar anotações: {erro}"


def send_telegram_message(message: str) -> str:
    """Envia uma mensagem real para Telegram usando o token do BotFather e o chat_id configurados no .env."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or "COLE_" in token or not chat_id or "COLE_" in chat_id:
        return "Telegram não configurado. Preencha TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID no arquivo .env."
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        response = requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=10)
        status = "enviado" if response.ok else f"falhou: {response.text}"
        conn = _connect_db()
        conn.execute(
            "INSERT INTO alerts (created_at, destination, message, status) VALUES (?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), str(chat_id), message, status),
        )
        conn.commit()
        conn.close()
        if response.ok:
            return "Mensagem enviada com sucesso para o Telegram."
        return f"Falha ao enviar para Telegram: {response.text}"
    except Exception as erro:
        return f"Erro ao enviar mensagem para Telegram: {erro}"


def get_crypto_news(limit: int = 5) -> str:
    """Busca notícias recentes de cripto via RSS público da CoinDesk e retorna títulos com links."""
    try:
        limit = int(limit)
        url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
        response = requests.get(url, timeout=10, headers={"User-Agent": "TradeSignalCopilot/1.0"})
        response.raise_for_status()
        root = ET.fromstring(response.content)
        items = root.findall("./channel/item")[:limit]
        if not items:
            return "Nenhuma notícia encontrada no RSS."
        linhas = []
        for item in items:
            title = item.findtext("title", default="Sem título")
            link = item.findtext("link", default="Sem link")
            pub_date = item.findtext("pubDate", default="Sem data")
            linhas.append(f"- {title}\n  Data: {pub_date}\n  Link: {link}")
        return "\n".join(linhas)
    except Exception as erro:
        return f"Erro ao buscar notícias: {erro}"
