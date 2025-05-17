from flask import Flask, render_template, send_file
from datetime import datetime
import os
from run_all import baixar_arquivo_aixm, processar_xmls

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar')
def gerar_openair():
    try:
        baixar_arquivo_aixm()
        processar_xmls()

        hoje = datetime.utcnow()
        nome = f"espaco_aereo_{hoje.strftime('%Y-%m-%d')}.txt"
        caminho = os.path.join("data", f"{hoje.year}", f"{str(hoje.month).zfill(2)}", nome)

        if os.path.exists(caminho):
            return send_file(caminho, as_attachment=True)
        else:
            return "Arquivo não encontrado.", 404
    except Exception as e:
        return f"Erro: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)