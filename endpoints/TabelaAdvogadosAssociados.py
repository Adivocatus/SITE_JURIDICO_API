from flask import Blueprint, jsonify, request, abort

from funcaoConectar import conectar

TabelaAdvogadosAssociados = Blueprint('tabelaadvogadosassociados', __name__)

#ROTAS PARA A TABELA TabelaAdvogadosAssociados
##ROTA GET
##############################################
@TabelaAdvogadosAssociados.route("/tabelaadvogadosassociados", methods=["GET"])
def listar_Cadastros():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT idAdvogadosAssociados, NomeAdvogadosAssociados, CPF_AdvogadosAssociados, ContatoAdvogadosAssociados, DadosJuridicosAdvogadosAssociados, RegistroAdvogadosAssociados FROM TabelaAdvogadosAssociados")
    dados = [
        {"idAdvogadosAssociados": row[0], "NomeAdvogadosAssociados": row[1], "CPF_AdvogadosAssociados": row[2], "ContatoAdvogadosAssociados": row[3], "DadosJuridicosAdvogadosAssociados": row[4], "RegistroAdvogadosAssociados": row [5]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

##ROTA INSERT
#############################################

@TabelaAdvogadosAssociados.route("/tabelaadvogadosassociados", methods=["POST"])
def criar_usuario():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"NomeAdvogadosAssociados", "CPF_AdvogadosAssociados", "ContatoAdvogadosAssociados", "DadosJuridicosAdvogadosAssociados", "RegistroAdvogadosAssociados"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tabelaadvogadosassociados (NomeAdvogadosAssociados, CPF_AdvogadosAssociados, ContatoAdvogadosAssociados, DadosJuridicosAdvogadosAssociados, RegistroAdvogadosAssociados)"
        "VALUES (?, ?, ?, ?, ?)",
        (dados["NomeAdvogadosAssociados"], dados["CPF_AdvogadosAssociados"], dados["ContatoAdvogadosAssociados"], dados["DadosJuridicosAdvogadosAssociados"], dados ["RegistroAdvogadosAssociados"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"idAdvogadosAssociados": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/tabelaadvogadosassociados/{novo_id}"
    return resposta

##ROTA UPDATE
#############################################
@TabelaAdvogadosAssociados.route("/tabelaadvogadosassociados/<int:idAdvogadosAssociados>", methods=["PUT", "PATCH"])
def atualizar_usuario(idAdvogadosAssociados):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"NomeAdvogadosAssociados", "CPF_AdvogadosAssociados", "ContatoAdvogadosAssociados", "DadosJuridicosAdvogadosAssociados", "RegistroAdvogadosAssociados"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"NomeAdvogadosAssociados", "CPF_AdvogadosAssociados", "ContatoAdvogadosAssociados", "DadosJuridicosAdvogadosAssociados", "RegistroAdvogadosAssociados"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(idAdvogadosAssociados)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE tabelaadvogadosassociadosSET {', '.join(set_clauses)} WHERE idAdvogadosAssociados = ?",
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
@TabelaAdvogadosAssociados.route("/tabelaadvogadosassociados/<int:idAdvogadosAssociados>", methods=["DELETE"])
def deletar_usuario(idAdvogadosAssociados):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM tabelaadvogadosassociados WHERE idAdvogadosAssociados = ?", (idAdvogadosAssociados))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Usuário não encontrado")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)