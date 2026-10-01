from flask import Flask, jsonify

from conectar.funcaoConectar import conectar

from endpoints.TabelaAdminstrador import TabelaAdminstrador
from endpoints.TabelaAdvogadosAssociados import TabelaAdvogadosAssociados
from endpoints.TabelaCliente import TabelaCliente

app = Flask(__name__)

app.register_blueprint(TabelaAdminstrador)
app.register_blueprint(TabelaAdvogadosAssociados)
app.register_blueprint(TabelaCliente)

if __name__ == "__main__":
    app.run(debug=True)