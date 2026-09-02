from flask import Blueprint, jsonify, request, abort

from funcaoConectar import conectar

TabelaAdminstrador = Blueprint('tabelaadministrador', __name__)

#ROTAS PARA A TABELA TabelaAreaAdminstrador
##ROTA GET
##############################################
@TabelaAdminstrador("/TabelaAreaAdminstrador", methods=["GET"])
def listar_Cadastros():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT idAreaAminstrador, GerenciarSite, CadastrarAdvogado, RealizarReunioesComAequipe, ElaborarModelosDeContratosPrestacaoServico, ElaborarFormulárioParaOsCliente, FROM TabelaAreaAdminstrador")
    dados = [
        {"idAdministrador": row[0], "NomeAdministrador": row[1], "SenhaAdministrador": row[2], "ContatoAdminstrador": row[3], "RegistroAdministrador": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

##ROTA INSERT
#############################################

@TabelaAdminstrador.route("/TabelaAdministrador", methods=["POST"])
def criar_usuario():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"NomeAdministrador", "SenhaAdministrador", "ContatoAdminstrador", "RegistroAdministrador"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
    "INSERT INTO TabelaAdministrador(NomeAdministrador, SenhaAdministrador, ContatoAdminstrador, RegistroAministrador)"
    "VALUES (?, ?, ?, ?)",
    (dados["NomeAdminstrador"], dados["SenhaAdminstrador"], dados["ContatoAdminstrador"], dados["RegistroAdminstrador"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"idTabelaAdminstrador": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/TabelaAminstrador/{novo_id}"
    return resposta

##ROTA UPDATE
#############################################
@TabelaAdminstrador.route("/TabelaAdminstrador/<int:TabelaAdministrador>", methods=["PUT", "PATCH"])
def atualizar_usuario(idTabelaAdminstrador):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"NomeAdminstrador", "SenhaAdminstrador", "ContatoAdminstrador", "RegistroAdminstrador"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"NomeAdminstrador", "SenhaAdminstrador", "ContatoAdminstrador", "RegistroAdministrador"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(idTabelaAdminstrador)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE TabelaAdminstradorSET {', '.join(set_clauses)} WHERE idTabelaAdminstrador = ?",
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
@TabelaAdminstrador.route("/TabelaAdminstrador/<int:idTabelaAdminstrador>", methods=["DELETE"])
def deletar_usuario(idTabelaAdminstrador):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM TabelaAdminstrador WHERE idTabelaAdminstrador = ?", (idTabelaAdminstrador))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Usuário não encontrado")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)