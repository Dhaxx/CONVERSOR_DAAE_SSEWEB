import conexao as cnx

cur_dest = cnx.get_cursor(cnx.conexao_destino)
cur_orig = cnx.get_cursor(cnx.conexao_origem)
# cur_aux = cnx.get_cursor(cnx.conexao_aux)

def cadastro():
    print("Cadastrando tramites...")
    insert = cur_dest.prep("""INSERT INTO se_ptramite (cod_emp_ptr, codigo_ptr, exercicio_ptr, item_ptr, setor_ant_ptr,
                                                       setor_atu_ptr, descricao_ptr, data_ptr, relator_ptr, recebido_ptr,
                                                       aberto_ptr, login_inc_ptr, dta_inc_ptr, data_rec_ptr, ultimo, excluido_ptr)
                               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""")

    cmd = cur_dest.execute("""SELECT * FROM se_pprotocolo sp""")

    for row in cmd.fetchall():
        cod_emp_ptr = 1
        codigo_ptr = row[1]
        exercicio_ptr = row[2] 
        item_ptr = 1
        setor_ant_ptr = 1
        setor_atu_ptr = 1
        descricao_ptr = row[6].upper()
        data_ptr = row[3].strftime("%Y-%m-%d")
        relato_ptr = row[5]
        recebido_ptr = 1
        aberto_ptr = 0
        login_inc_ptr = "CONVERSAO"
        dta_inc_ptr = data_ptr
        data_rec_ptr = data_ptr
        ultimo = 1
        excluido_ptr = 'N'
                
        cur_dest.execute(insert,(cod_emp_ptr, codigo_ptr, exercicio_ptr, item_ptr, setor_ant_ptr,
                                setor_atu_ptr, descricao_ptr, data_ptr, relato_ptr, recebido_ptr,
                                aberto_ptr, login_inc_ptr, dta_inc_ptr, data_rec_ptr, ultimo, excluido_ptr))
    cnx.commit()


        

