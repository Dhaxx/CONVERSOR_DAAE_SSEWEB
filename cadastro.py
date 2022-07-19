import conexao as cnx

cur_dest = cnx.get_cursor(cnx.conexao_destino)
cur_orig = cnx.get_cursor(cnx.conexao_origem)

def cad_setor():
    print("Cadastrando setores...")

    insert = cur_dest.prep("INSERT INTO se_setor (cod_emp_set, cod_set, descricao_set, sigla_set, login_inc_set) values (?, ?, ?, ?, ?)")

    cur_orig.execute("""SELECT * FROM SETORES s""") 

    i = cur_dest.execute("""SELECT MAX(cod_set) FROM se_setor""").fetchone()[0]

    for row in cur_orig:
        i += 1
        cod_emp_set = 1
        cod_set = i
        descricao_set = row[1]
        sigla_set = row[2]
        login_inc_set = "CONVERSAO"

        cur_dest.execute(insert,(cod_emp_set, cod_set, descricao_set, sigla_set, login_inc_set))
    cnx.commit()

def cad_assunto():
    print("Cadastrando assuntos...")

    insert = cur_dest.prep("INSERT INTO se_assunto(cod_emp_asu, cod_asu, descricao_asu, login_inc_asu, ativado_asu, mobile_asu) VALUES (?,?,?,?,?,?)")
    cur_orig.execute("""SELECT * FROM ASSUNTOS a order by as_codigo""")

    i = 0
    for row in cur_orig:
        i += 1
        cod_emp_asu = 1
        cod_asu = i
        descricao_asu = row[1]
        login_inc_asu = "CONVERSAO"
        ativado_asu = "S"
        mobile_asu = "N"

        cur_dest.execute(insert,(cod_emp_asu, cod_asu, descricao_asu, login_inc_asu, ativado_asu, mobile_asu))
    cnx.commit()

def tipo_doc():
    print("Inserindo tipos de documentos...")

    insert = cur_dest.prep("INSERT INTO se_tipodoc (cod_emp_tdc, cod_tdc, descricao_tdc, login_inc_tdc) VALUES(?, ?, ?, ?)")
    # insert_protocolo = cur_dest.prep("INSERT INTO se_tipodoc (cod_emp_tdc, cod_tdc, descricao_tdc, login_inc_tdc) VALUES(1, 1, 'PROTOCOLO/PROCESSO', 'CONVERSAO');")
    cur_orig.execute("""SELECT * FROM RECEITAS r""")

    i = 1

    # cur_dest.execute(insert_protocolo)

    for row in cur_orig:
        i += 1
        cod_emp_tdc = 1
        cod_tdc = i
        descricao_tdc = row[1]
        login_inc_tdc = "CONVERSAO"

        cur_dest.execute(insert,(cod_emp_tdc, cod_tdc, descricao_tdc, login_inc_tdc))
    cnx.commit()

def cad_cidades():
    print("Cadastrando cidades...")

    insert = cur_dest.prep("INSERT INTO gr_cidade (cod_cid, nome_cid, uf_cid, popula_cid) VALUES (?, ?, ?, ?)")
    cur_orig.execute("""SELECT DISTINCT(gr_cidade), gr_uf FROM guias""")

    i = 0

    for row in cur_orig:
        i += 1
        cod_cid = str(i).zfill(7)
        nome_cid = row[0].upper()
        uf_cid = row[1].upper()
        populacao_cid = 0

        cur_dest.execute(insert,(cod_cid, nome_cid, uf_cid, populacao_cid))
    cnx.commit()

def cad_bairro():
    print("Cadastrando bairros...")

    insert = cur_dest.prep("INSERT INTO gr_bairro (cod_emp_bai, cod_bai, nome_bai) VALUES (?, ?, ?)")
    cur_orig.execute("""SELECT DISTINCT(GR_BAIRRO) FROM guias""")

    cod_bai = 0

    for row in cur_orig:
        cod_emp_bai = 1
        cod_bai += 1
        nome_bai = row[0].upper()

        cur_dest.execute(insert,(cod_emp_bai, cod_bai, nome_bai))
    cnx.commit()

def cad_logradouro():
    print("Cadastrando logradouros...")

    insert = cur_dest.prep("INSERT INTO gr_logra(cod_emp_log, cod_log, cod_bair_log, cep_log, nome_log) VALUES (?, ?, ?, ?, ?)")
    cur_orig.execute("""SELECT DISTINCT(GR_END), GR_CEP, GR_BAIRRO FROM guias""")

    i = 0

    for row in cur_orig:
        i += 1
        cod_emp_log = 1
        cod_log = i
        cod_bair_log = cur_dest.execute("""SELECT cod_bai FROM gr_bairro WHERE nome_bai = '{}'""".format(row[2].upper())).fetchone()[0]
        cep_log = row[1]
        nome_log = row[0].upper() if len(row[1]) <= 60 else row[0][:60]

        cur_dest.execute(insert,(cod_emp_log, cod_log, cod_bair_log, cep_log, nome_log))
    cnx.commit()

def cad_contribuinte():
    cur_dest.execute("""delete from GR_CONTRIBUINTES""")
    print("Cadastrando contribuintes...")
    global cod_cnt_ant 
    cod_cnt_ant = ""

    insert = cur_dest.prep("""INSERT INTO gr_contribuintes(cod_emp_cnt, cod_cnt, cnpj_cnt,
                                                           nome_cnt, cod_log_cnt, nom_log_cnt,
                                                           numero_cnt, nom_bai_cnt, cep_cnt, 
                                                           cod_cid_cnt, nom_cid_cnt, rg_cnt, 
                                                           sexo_cnt, sequencial_cnt)
                              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""")
    
    sequencial_cnt = 0

    cur_orig.execute("""SELECT * FROM CONTRIBUINTES a""")

    for row in cur_orig.fetchall():
        cod_emp_cnt = 1
        cod_cnt = row[0]
        cnpj_cnt = row[4]
        nome_cnt = row[1]
        cod_log_cnt = cur_dest.execute("""SELECT cod_log FROM gr_logra WHERE nome_log = '{}'""".format(row[6].upper())).fetchone()[0]
        nom_log_cnt = row[6].upper()
        numero_cnt = row[7]
        nom_bai_cnt = row[9]
        cep_cnt = row[12]
        cod_cid_cnt = cur_dest.execute("""SELECT cod_cid FROM gr_cidade WHERE nome_cid = '{}'""".format(row[10].upper())).fetchone()[0]
        nom_cid_cnt = row[10].upper()
        rg_cnt = row[3]
        sexo_cnt = row[2]
        sequencial_cnt += 1

        cur_dest.execute(insert,(cod_emp_cnt, cod_cnt, cnpj_cnt, nome_cnt, cod_log_cnt, nom_log_cnt, numero_cnt,
                         nom_bai_cnt, cep_cnt, cod_cid_cnt, nom_cid_cnt, rg_cnt, sexo_cnt, sequencial_cnt))
    cnx.commit()