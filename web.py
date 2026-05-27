from flask import Flask, render_template, request
from dotenv import load_dotenv
from fast_router import fast_route

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    resposta = ""
    pergunta = ""

    if request.method == "POST":
        pergunta = request.form.get("pergunta", "").strip()

        if pergunta:
            try:
                resposta = fast_route(pergunta)

                if not resposta:
                    resposta = (
                        "Comando não identificado pelo modo rápido. "
                        "Tente: preço, notícias, risco, diário ou Telegram."
                    )

            except Exception as erro:
                resposta = f"Erro: {erro}"

    return render_template("index.html", pergunta=pergunta, resposta=resposta)


if __name__ == "__main__":
    app.run(debug=False)