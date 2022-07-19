import conexao as cnx
from conexao import conexao_destino

cur_dest = cnx.get_cursor(conexao_destino)

def limpa_tabelas():
    print("Limpando tabelas...")
    tabelas = ["delete from SE_PDOCUMENTOS",
               "delete from SE_CARGOS",
               "delete from SE_ASSUNTO",
               "delete from SE_PTRAMITE",
               "delete from SE_PPROTOCOLO",
               "delete from GR_CONTRIBUINTES",
               "delete from GR_LOGRA",
               "delete from GR_BAIRRO",
               "delete from GR_CIDADE",
               "delete from SE_SSE_PERMISSAO WHERE COD_USR_PER > 4",
               "delete from SE_USER_SETOR",
               "delete from SE_SSE_USUARIO",
               "delete from SE_SETOR",
               "delete from SE_TIPODOC"]

    for tabela in tabelas:
        cur_dest.execute(tabela)      
    cnx.commit()