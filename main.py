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

def lista_elementos():
    cursor.execute('SELECT * FROM patogeno;')
    r = cursor.fetchone()
    for r in cursor:
        print(r)

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
        print("Sistoma inserido com sucesso!")
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

def menu():
    while True:
        print("\nMenu:")
        print("1. Inserir Doença")
        print("2. Inserir Sintoma")
        print("3. Inserir Nome Popular")
        print("4. Inserir Apresentação")
        print("5. Inserir Patogeno")
        print("6. Sair")
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
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()

conexao.close()
cursor.close()