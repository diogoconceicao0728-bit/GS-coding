import re
from tools import (
    get_crypto_price,
    calculate_trade_risk,
    save_trade_note,
    list_trade_notes,
    send_telegram_message,
    get_crypto_news,
)


def fast_route(texto: str):
    """
    Roteador rápido para executar tools diretamente quando a intenção do usuário
    for clara. Isso reduz latência na interface web.
    """
    if not texto:
        return None

    t = texto.lower()

    if "preço" in t or "preco" in t or "cotação" in t or "cotacao" in t:
        match = re.search(r"\b([a-z]{2,10}usdt)\b", t)
        symbol = match.group(1).upper() if match else "BTCUSDT"
        return get_crypto_price(symbol)

    if "notícia" in t or "noticia" in t or "news" in t:
        match = re.search(r"\b(\d+)\b", t)
        limit = int(match.group(1)) if match else 3
        return get_crypto_news(limit)

    if "risco" in t and ("banca" in t or "entrada" in t or "stop" in t):
        numeros = re.findall(r"\d+(?:[\.,]\d+)?", texto)
        numeros = [float(n.replace(",", ".")) for n in numeros]

        if len(numeros) >= 4:
            banca = numeros[0]
            risco = numeros[1]
            entrada = numeros[2]
            stop = numeros[3]
            return calculate_trade_risk(banca, risco, entrada, stop)

        return "Envie banca, risco %, entrada e stop. Exemplo: Calcule risco com banca 1000, risco 2%, entrada 65000 e stop 64000"

    if "salve" in t or "salvar" in t or "anotação" in t or "anotacao" in t:
        symbol_match = re.search(r"\b([a-z]{2,10}usdt)\b", t)
        symbol = symbol_match.group(1).upper() if symbol_match else "BTCUSDT"

        bias = "neutro"
        if "comprado" in t or "compra" in t or "long" in t:
            bias = "comprado"
        elif "vendido" in t or "venda" in t or "short" in t:
            bias = "vendido"

        numeros = re.findall(r"\d+(?:[\.,]\d+)?", texto)
        numeros = [float(n.replace(",", ".")) for n in numeros]

        entry = numeros[0] if len(numeros) >= 1 else None
        stop = numeros[1] if len(numeros) >= 2 else None
        target = numeros[2] if len(numeros) >= 3 else None

        return save_trade_note(symbol, bias, entry, stop, target, texto)

    if "liste" in t or "listar" in t or "diário" in t or "diario" in t or "anotações" in t or "anotacoes" in t:
        return list_trade_notes(5)

    if "telegram" in t or "envie" in t or "enviar" in t:
        mensagem = texto

        if "dizendo:" in texto.lower():
            mensagem = texto.split(":", 1)[1].strip()

        return send_telegram_message(mensagem)

    return None