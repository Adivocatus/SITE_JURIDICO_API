from flask import Blueprint, jsonify, request, abort

from funcaoConectar import conectar

TabelaCliente = Blueprint('tabelacliente', __name__)

#ROTAS PARA A TABELA TabelaCliente
##ROTA GET,
#alguns erros de escrita!
##############################################
@TabelaCliente("/tabelacliente", methods=["GET"])
def listar_Cadastros():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT idCliente, NomeCliente, SenhaCliente, CPF_Cliente, EnderecoClientes, ContatoCliente, DadosJuridicosClientes FROM TabelaCliente") #cliente
    dados = [
        {"idCliente": row[0], "NomeCliente": row[1], "SenhaCliente": row[2], "CPF_Cliente": row[3], "EnderecoClientes": row[4], "ContatoCliente": row[5], "DadosJuridicosClientes": row[6]} #administrador
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

##ROTA INSERT
#############################################

@TabelaCliente.route("/tabelacliente", methods=["POST"])
def criar_usuario():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"NomeCliente", "SenhaCliente", "CPF_Cliente", "EnderecoClientes", "ContatoCliente", "DadosJuridicosClientes"}#adicionar registro ao banco ou corrigir.
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
    "INSERT INTO tabelacliente(NomeCliente, SenhaCliente, CPF_Cliente, EnderecoClientes, ContatoCliente, DadosJuridicosClientes)"
    "VALUES (?, ?, ?, ?)",
    (dados["NomeCliente"], dados["SenhaCliente"], dados["CPF_Cliente"], dados["EnderecoClientes"], dados["ContatoCliente"], dados["DadosJuridicosClientes"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"idCliente": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/tabelacliente/{novo_id}"
    return resposta

##ROTA UPDATE
#############################################
@TabelaCliente.route("/tabelacliente/<int:idCliente>", methods=["PUT", "PATCH"])
def atualizar_usuario(idCliente):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"NomeCliente", "SenhaCliente", "CPF_Cliente", "EnderecoClientes", "ContatoCliente", "DadosJuridicosClientes"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"NomeCliente", "SenhaCliente", "CPF_Cliente", "EnderecoClientes", "ContatoCliente", "DadosJuridicosCliente"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(idCliente)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE tabelaclienteSET {', '.join(set_clauses)} WHERE idCliente = ?",
        tuple(valores)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Usuário não encontrado")

    conn.close()
    # 204 = No Content, mas você pode devolver 200 com o JSON atualizado se preferir
    return ("", 204)


##ROTA DELETE
#############################################
@TabelaCliente.route("/tabelacliente/<int:idCliente>", methods=["DELETE"])
def deletar_usuario(idCliente):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM tabelacliente WHERE idCliente = ?", (idCliente))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Usuário não encontrado")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)