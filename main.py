import mysql.connector
import logging
from mysql.connector import errorcode

logging.basicConfig(filename='sistema.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

def log_operacao(operacao, detalhes=""):
    logging.info(f"{operacao} - {detalhes}")

conexao = mysql.connector.connect(host='localhost',
                                  database='doenca',
                                  user='root',
                                  password='pardal5link')

if conexao.is_connected():
    print('Conectado ao Banco de Dados!')
    cursor = conexao.cursor()
else:
    print('Não foi possível conectar ao Banco de Dados')
    
add_patogeno = ("INSERT INTO patogeno"
              "(nome, tipo)"
              "VALUES (%(nome)s, %(tipo)s)")

add_doenca = ("INSERT INTO doença"
              "(nome_tecnico, CID, id_patogeno)"
              "VALUES (%(nome_tecnico)s, %(CID)s, %(id_patogeno)s)")

add_sintoma = ("INSERT INTO sintomas"
               "(nome)"
               "VALUES (%(nome)s)")

add_nome_popular = ("INSERT INTO nomes_populares"
                    "(doença_id, nome)"
                    "VALUES (%(doença_id)s, %(nome)s)")

add_apresenta = ("INSERT INTO apresenta"
                 "(doença_id, sintoma_id, frequencia)"
                 "VALUES (%(doença_id)s, %(sintoma_id)s, %(frequencia)s)")

def inserir_patogeno():
    data_patogeno = {
        'nome': input("Digite o nome do patogeno: "),
        'tipo': input("Digite o tipo do patogeno: ")
    }
    try:
        cursor.execute(add_patogeno, data_patogeno)
        conexao.commit()
        print("Patogeno inserido com sucesso!")
        log_operacao("Insercao de Patogeno", f"Nome: {data_patogeno['nome']}, Tipo: {data_patogeno['tipo']}")
    except mysql.connector.Error as err:
        if err:
            print(f"Erro: {err}")

def inserir_doenca():
    data_doenca = {
        'nome_tecnico': input("Digite o nome técnico da doença: "),
        'CID': input("Digite o CID da doença: "),
        'id_patogeno': int(input("Digite o ID do patógeno: "))
    }
    try:
        cursor.execute(add_doenca, data_doenca)
        conexao.commit()
        print("Doença inserida com sucesso!")
        log_operacao("Insercao de Doenca", f"Nome Tecnico: {data_doenca['nome_tecnico']}, CID: {data_doenca['CID']}")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
            print("Erro: O patógeno com o ID fornecido não existe.")
        else:
            print(f"Erro: {err}")

def inserir_sintoma():
    data_sintoma = {
        'nome': input("Digite o nome do sintoma: ")
    }
    try:
        cursor.execute(add_sintoma, data_sintoma)
        conexao.commit()
        print("Sintoma inserido com sucesso!")
        log_operacao("Insercao de Sintoma", f"Nome: {data_sintoma['nome']}")
    except mysql.connector.Error as err:
        if err:
            print(f"Erro: {err}")

def inserir_nome_popular():
    data_nome_popular = {
        'doença_id': int(input("Digite o ID da doença para o nome popular: ")),
        'nome': input("Digite o nome popular: ")
    }
    try:
        cursor.execute(add_nome_popular, data_nome_popular)
        conexao.commit()
        print("Nome popular inserido com sucesso!")
        log_operacao("Insercao de Nome Popular", f"Doenca ID: {data_nome_popular['doença_id']}, Nome: {data_nome_popular['nome']}")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
            print("Erro: A doença com o ID fornecido não existe.")
        else:
            print(f"Erro: {err}")

def inserir_apresenta():
    data_apresenta = {
        'doença_id': int(input("Digite o ID da doença: ")),
        'sintoma_id': int(input("Digite o ID do sintoma: ")),
        'frequencia': input("Digite a frequência: ")
    }
    try:
        cursor.execute(add_apresenta, data_apresenta)
        conexao.commit()
        print("Dados inseridos com sucesso!")
        log_operacao("Insercao de Apresentacao", f"Doenca ID: {data_apresenta['doença_id']}, Sintoma ID: {data_apresenta['sintoma_id']}, Frequencia: {data_apresenta['frequencia']}")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
            print("Erro: A doença ou sintoma com o ID fornecido não existe.")
        else:
            print(f"Erro: {err}")

def lista_doenca():
    try:
        cursor.execute('SELECT * FROM doença;')
        linhas = cursor.fetchall()
        if linhas:
            print("+----+---------------------+----------+------------+")
            print("| ID | Nome Técnico        | CID      | ID Patógeno|")
            print("+----+---------------------+----------+------------+")
            for (id, nome_tecnico, CID, id_patogeno) in linhas:
                print(f"| {str(id).ljust(2)} | {nome_tecnico.ljust(19)} | {CID.ljust(8)} | {str(id_patogeno).ljust(10)} |")
            print("+----+---------------------+----------+------------+")
        else:
            print("Nenhuma doença encontrada.")
        log_operacao("Listagem de Doencas")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")

def lista_sintomas():
    try:
        cursor.execute('SELECT * FROM sintomas;')
        linhas = cursor.fetchall()
        if linhas:
            print("+----+---------------------+")
            print("| ID | Sintoma             |")
            print("+----+---------------------+")
            for (id, nome) in linhas:
                print(f"| {str(id).ljust(2)} | {nome.ljust(19)} | ")
            print("+----+---------------------+")
        else:
            print("Nenhum sintoma encontrado.")
        log_operacao("Listagem de Sintomas")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")

def pesquisar_doenca():
    print("1. Nome tecnico")
    print("2. Nome popular")
    print("3. CID")
    print("4. Patogeno")
    criterio = input("Pesquisar por: ")
    if criterio not in ["1", "2", "3", "4"]:
        print("Critério indefinido.")
        return
    
    valor = input(f"Digite conforme o criterio de pesquisa selecionado: ")

    if criterio == "1":
        query = "SELECT * FROM doença WHERE nome_tecnico = %s"
    elif criterio == "2":
        query = ("SELECT d.* FROM doença d "
                 "JOIN nomes_populares np ON d.id = np.doença_id "
                 "WHERE np.nome = %s")
    elif criterio == "3":
        query = "SELECT * FROM doença WHERE CID = %s"
    elif criterio == "48":
        query = ("SELECT d.* FROM doença d "
                 "JOIN patogeno p ON d.id_patogeno = p.id "
                 "WHERE p.nome = %s")

    try:
        cursor.execute(query, (valor,))
        r = cursor.fetchall()
        if not r:
            print("Nenhuma doença encontrada com o critério fornecido.")
        else:
            print("+----+---------------------+----------+------------+-----------------------------------------------------------------------------------+")
            print("| ID | Nome Técnico        | CID      | ID Patógeno| Sintomas                                                                          |")
            print("+----+---------------------+----------+------------+-----------------------------------------------------------------------------------+")

            for (id, nome_tecnico, CID, id_patogeno) in r:
                sintomas = listar_sintomas(id)
            print(f"| {str(id).ljust(2)} | {nome_tecnico.ljust(19)} | {CID.ljust(8)} | {str(id_patogeno).ljust(10)} | {sintomas.ljust(44)}                |")
            print("+----+---------------------+----------+------------+-----------------------------------------------------------------------------------+")
        log_operacao("Pesquisa de Doenca", f"Criterio: {criterio}, Valor: {valor}")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def listar_sintomas(doenca_id):
    try:
        query = ("""
            SELECT GROUP_CONCAT(CONCAT(s.nome, '(', a.frequencia, ')') 
            ORDER BY FIELD(a.frequencia, 'muito comum', 'comum', 'pouco comum', 'raro', 'muito raro')) AS sintomas
            FROM sintomas s
            JOIN apresenta a ON s.id = a.sintoma_id
            WHERE a.doença_id = %s
        """)
        cursor.execute(query, (doenca_id,))
        row = cursor.fetchone()

        if row and row[0]:
            return row[0]
        else:
            return "Nenhum sintoma encontrado"

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return "Erro ao buscar sintomas"


def menu():
    while True:
        print("\nMenu:")
        print("1. Inserir Doença")
        print("2. Inserir Sintoma")
        print("3. Inserir Nome Popular")
        print("4. Inserir Apresentação")
        print("5. Inserir Patogeno")
        print("6. Listar Doenças")
        print("7. Listar Sintomas")
        print("8. Pesquisar Doença")
        print("0. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            inserir_doenca()
        elif escolha == '2':
            inserir_sintoma()
        elif escolha == '3':
            inserir_nome_popular()
        elif escolha == '4':
            inserir_apresenta()
        elif escolha == '5':
            inserir_patogeno()
        elif escolha == '6':
            lista_doenca()
        elif escolha == '7':
            lista_sintomas()    
        elif escolha == '8':
            pesquisar_doenca()
        elif escolha == '0':
            log_operacao("Saida do sistema")
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()

conexao.close()
cursor.close()