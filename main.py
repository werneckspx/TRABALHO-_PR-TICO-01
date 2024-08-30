import mysql.connector
from mysql.connector import errorcode

conexao = mysql.connector.connect(host='localhost',
                                  database='doenca',
                                  user='root',
                                  password='felipe')

if conexao.is_connected():
    print('Conectado ao Banco de Dados!')
    cursor = conexao.cursor()
else:
    print('Não foi possível conectar ao Banco de Dados')
    
add_patogeno = ("INSERT INTO patogeno"
              "(id, nome, tipo)"
              "VALUES (%(id)s, %(nome)s, %(tipo)s)")

add_doenca = ("INSERT INTO doença"
              "(id, nome_tecnico, CID, id_patogeno)"
              "VALUES (%(id)s, %(nome_tecnico)s, %(CID)s, %(id_patogeno)s)")

add_sintoma = ("INSERT INTO sintomas"
               "(id, nome)"
               "VALUES (%(id)s, %(nome)s)")

add_nome_popular = ("INSERT INTO nomes_populares"
                    "(doença_id, nome)"
                    "VALUES (%(doença_id)s, %(nome)s)")

add_apresenta = ("INSERT INTO apresenta"
                 "(doença_id, sintoma_id, frequencia)"
                 "VALUES (%(doença_id)s, %(sintoma_id)s, %(frequencia)s)")

def inserir_patogeno():
    data_patogeno = {
        'id': int(input("Digite o ID do patogeno: ")),
        'nome': input("Digite o nome do patogeno: "),
        'tipo': input("Digite o nome do patogeno: ")
    }
    try:
        cursor.execute(add_patogeno, data_patogeno)
        conexao.commit()
        print("Patogeno inserido com sucesso!")
    except mysql.connector.Error as err:
        if err:
            print(f"Erro: {err}")

def inserir_doenca():
    data_doenca = {
        'id': int(input("Digite o ID da doença: ")),
        'nome_tecnico': input("Digite o nome técnico da doença: "),
        'CID': input("Digite o CID da doença: "),
        'id_patogeno': int(input("Digite o ID do patógeno: "))
    }
    try:
        cursor.execute(add_doenca, data_doenca)
        conexao.commit()
        print("Doença inserida com sucesso!")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
            print("Erro: O patógeno com o ID fornecido não existe.")
        else:
            print(f"Erro: {err}")

def inserir_sintoma():
    data_sintoma = {
        'id': int(input("Digite o ID do sintoma: ")),
        'nome': input("Digite o nome do sintoma: ")
    }
    try:
        cursor.execute(add_sintoma, data_sintoma)
        conexao.commit()
        print("Sintoma inserido com sucesso!")
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
    except mysql.connector.Error as err:
        print(f"Erro: {err}")

def pesquisar_doenca():
    criterio = input("Pesquisar por (nome_tecnico, nome_popular, CID, patogeno): ")
    if criterio not in ["nome_tecnico", "nome_popular", "CID", "patogeno"]:
        print("Critério indefinido.")
        return
    
    valor = input(f"Digite o valor para {criterio}: ")

    if criterio == "nome_tecnico":
        query = "SELECT * FROM doença WHERE nome_tecnico = %s"
    elif criterio == "nome_popular":
        query = ("SELECT d.* FROM doença d "
                 "JOIN nomes_populares np ON d.id = np.doença_id "
                 "WHERE np.nome = %s")
    elif criterio == "CID":
        query = "SELECT * FROM doença WHERE CID = %s"
    elif criterio == "patogeno":
        query = ("SELECT d.* FROM doença d "
                 "JOIN patogeno p ON d.id_patogeno = p.id "
                 "WHERE p.nome = %s")

    try:
        cursor.execute(query, (valor,))
        r = cursor.fetchall()
        if not r:
            print("Nenhuma doença encontrada com o critério fornecido.")
        else:
            print("+----+---------------------+----------+------------+----------------------------------------------+")
            print("| ID | Nome Técnico        | CID      | ID Patógeno| Sintomas                                     |")
            print("+----+---------------------+----------+------------+----------------------------------------------+")

            for (id, nome_tecnico, CID, id_patogeno) in r:
                sintomas = listar_sintomas(id)
                print(f"| {str(id).ljust(2)} | {nome_tecnico.ljust(19)} | {CID.ljust(8)} | {str(id_patogeno).ljust(10)} | {sintomas.ljust(44)} |")
                print("+----+---------------------+----------+------------+----------------------------------------------+")

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
        print("6. Listar Doença")
        print("7. Pesquisar Doença")
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
            pesquisar_doenca()
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()

conexao.close()
cursor.close()
