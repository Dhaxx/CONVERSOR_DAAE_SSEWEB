from datetime import datetime
import conexao as cnx

cur_dest = cnx.get_cursor(cnx.conexao_destino)
cur_orig = cnx.get_cursor(cnx.conexao_origem)
# cur_aux = cnx.get_cursor(cnx.conexao_aux)

def cadastro():
    print("Cadastrando protocolos...")

    insert = cur_dest.prep("""INSERT INTO se_pprotocolo (cod_emp_prt, codigo_prt, exercicio_prt, data_prt,
                                                         responsavel_prt, assunto_prt, dados_prt, login_inc_prt, dta_inc_prt,
                                                         login_alt_prt, dta_alt_prt, materia_tipo_prt, setor_prt, sigilo_prt,
                                                         interessado_prt,cod_asu_prt, chave_web_prt, tipo_prt, protocolo_prt)
                              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""")

    cmd = cur_orig.execute("""SELECT * FROM GUIAS g""")

    for row in cmd:
        cod_emp_prt = 1
        codigo_prt = row[1]
        exercicio_prt = row[0]
        data_prt = row[2].strftime("%Y-%m-%d")
        responsavel_prt = row[5]
        assunto_prt = cur_dest.execute("""Select descricao_asu from se_assunto where cod_asu = '{}'""".format(row[3])).fetchone()[0]
        dados_prt = row[6].upper()
        login_inc_prt = "CONVERSAO"
        dta_inc_prt = data_prt
        login_alt_prt = "CONVERSAO"
        dta_alt_prt = data_prt
        materia_tipo_prt = "EXTERNA"
        setor_prt =  1
        sigilo_prt = "N"
        interessado_prt = str(row[4])
        cod_asu_prt = row[3]
        chave_web_prt = None
        tipo_prt = 1
        protocolo_prt = str(row[1])

        cur_dest.execute(insert,(cod_emp_prt, codigo_prt, exercicio_prt, data_prt, responsavel_prt, assunto_prt,
                       dados_prt, login_inc_prt, dta_inc_prt, login_alt_prt, dta_alt_prt, materia_tipo_prt, setor_prt,
                       sigilo_prt, interessado_prt, cod_asu_prt, chave_web_prt, tipo_prt, protocolo_prt))
    cnx.commit()