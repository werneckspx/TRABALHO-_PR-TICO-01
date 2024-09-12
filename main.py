import mysql.connector
import logging
from mysql.connector import errorcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

global arquivos
arquivos = 0

global arquivos2
arquivos2 = 0

#----------------------------------------------------------------------------------------------------------------------------------------------#
# CONEXÃO E ORGANIZAÇÃO DO BANCO DE DADOS#

logging.basicConfig(filename='sistema.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

def log_operacao(operacao, detalhes=""):
    logging.info(f"{operacao} - {detalhes}")

conexao = mysql.connector.connect(host='localhost',
                                  database='doenca',
                                  user='root',
                                  password='')

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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# QUESTÃO 1 #

def inserir_patogeno():
    data_patogeno = {
        'nome': input("Digite o nome do patógeno: "),
        'tipo': input("Digite o tipo do patógeno: ")
    }
    try:
        cursor.execute(add_patogeno, data_patogeno)
        conexao.commit()
        print("Patógeno inserido com sucesso!")
        log_operacao("Insercao de Patogeno", f"Nome: {data_patogeno['nome']}, Tipo: {data_patogeno['tipo']}")
        return cursor.lastrowid  # Retorna o ID do patógeno recém inserido
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return None

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
            
def inserir_doenca():
    try:
        log_operacao("Inicio de Insercao de Doenca")
        data_doenca = {
            'nome_tecnico': input("Digite o nome técnico da doença: "),
            'CID': input("Digite o CID da doença: ")
        }
        log_operacao("Entrada de Dados da Doenca", f"Nome Tecnico: {data_doenca['nome_tecnico']}, CID: {data_doenca['CID']}")
        lista_patogeno()
        log_operacao("Listagem de Patogenos", "Usuario visualizou a lista de patogenos.")
        
        try:
            id_patogeno = int(input("Digite o ID do patógeno (0 para inserir novo patógeno): "))
            log_operacao("Selecao de Patogeno", f"ID Patogeno Selecionado: {id_patogeno}")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro.")
            log_operacao("Erro na Entrada do ID do Patogeno", "Entrada nao eh um numero inteiro.")
            return

        if id_patogeno == 0:
            log_operacao("Insercao de Novo Patogeno", "Usuario optou por inserir um novo patogeno.")
            id_patogeno = inserir_patogeno()
            if id_patogeno is None:
                print("Erro ao inserir patógeno. Processo cancelado.")
                log_operacao("Erro na Insercao de Patogeno", "Usuario cancelou o processo apos erro.")
                return
            else:
                log_operacao("Novo Patogeno Inserido", f"ID do Novo Patogeno: {id_patogeno}")
        
        data_doenca['id_patogeno'] = id_patogeno
        
        cursor.execute(add_doenca, data_doenca)
        conexao.commit()
        print("Doença inserida com sucesso!")
        log_operacao("Insercao de Doenca", f"Nome Tecnico: {data_doenca['nome_tecnico']}, CID: {data_doenca['CID']}, ID Patogeno: {id_patogeno}")
        
        id_doenca = cursor.lastrowid

        while True:
            opcao = input("Deseja inserir um nome popular para a doença? (s/n): ").lower()
            log_operacao("Opcao de Inserir Nome Popular", f"Escolha: {opcao}")
            if opcao in ['s', 'n']:
                break
            else:
                print("Entrada inválida. Por favor, insira 's' para sim ou 'n' para não.")
        
        if opcao == 's':
            inserir_nome_popular_com_parametro(id_doenca)

        while True:
            opcao = input("Deseja associar sintomas à doença? (s/n): ").lower()
            log_operacao("Opcao de Associar Sintomas", f"Escolha: {opcao}")
            if opcao in ['s', 'n']:
                break
            else:
                print("Entrada inválida. Por favor, insira 's' para sim ou 'n' para não.")
        
        if opcao == 's':
            lista_sintomas()
            inserir_apresenta_com_parametro(id_doenca)

            while True:
                while True:
                    adicionar_mais_sintomas = input("Deseja adicionar mais sintomas? (s/n): ").lower()
                    if adicionar_mais_sintomas in ['s', 'n']:
                        break
                    else:
                        print("Entrada inválida. Por favor, insira 's' para sim ou 'n' para não.")
                
                if adicionar_mais_sintomas == 's':
                    lista_sintomas()
                    inserir_apresenta_com_parametro(id_doenca)
                else:
                    break
        
        log_operacao("Finalizacao da Insercao de Doenca", f"Doenca ID: {id_doenca} inserida com sucesso.")
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
            print("Erro: o patógeno com o ID fornecido não existe.")
            log_operacao("Erro ao Inserir Doenca", f"Patogeno com ID {id_patogeno} nao existe. Erro: {err}")
        else:
            print(f"Erro: {err}")
            log_operacao("Erro ao Inserir Doenca", f"Erro: {err}")
    
    except Exception as e:
        print(f"Erro inesperado: {e}")
        log_operacao("Erro Inesperado ao Inserir Doenca", f"Erro: {e}")


def inserir_nome_popular_com_parametro(id_doenca):
    data_nome_popular = {
        'doença_id': id_doenca,
        'nome': input("Digite o nome popular: ")
    }
    try:
        cursor.execute(add_nome_popular, data_nome_popular)
        conexao.commit()
        print("Nome popular inserido com sucesso!")
        log_operacao("Insercao de Nome Popular", f"Doenca ID: {data_nome_popular['doença_id']}, Nome: {data_nome_popular['nome']}")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")

def inserir_apresenta_com_parametro(id_doenca):
    data_apresenta = {
        'doença_id': id_doenca,
        'sintoma_id': int(input("Digite o ID do sintoma: "))
    }
    
    frequencias_permitidas = ['pouco comum', 'comum', 'muito comum', 'raro', 'muito raro']

    while True:
        frequencia = input("Digite a frequência (pouco comum, comum, muito comum, raro, muito raro): ").lower()
        if frequencia in frequencias_permitidas:
            data_apresenta['frequencia'] = frequencia
            break
        else:
            print("Entrada inválida. Por favor, insira uma das opções: pouco comum, comum, muito comum, raro, muito raro.")
    
    try:
        cursor.execute(add_apresenta, data_apresenta)
        conexao.commit()
        print("Associação de sintoma inserida com sucesso!")
        log_operacao("Insercao de Associacao de Sintoma", f"Doenca ID: {data_apresenta['doença_id']}, Sintoma ID: {data_apresenta['sintoma_id']}, Frequencia: {data_apresenta['frequencia']}")
    except mysql.connector.Error as err:
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
    while True:
        try:
            doenca_id = int(input("Digite o ID da doença: "))
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro válido para o ID da doença.")
    
    while True:
        try:
            sintoma_id = int(input("Digite o ID do sintoma: "))
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro válido para o ID do sintoma.")
    
    frequencias_permitidas = ['pouco comum', 'comum', 'muito comum', 'raro', 'muito raro']

    while True:
        frequencia = input("Digite a frequência (pouco comum, comum, muito comum, raro, muito raro): ").lower()
        if frequencia in frequencias_permitidas:
            break
        else:
            print("Entrada inválida. Por favor, insira uma das opções: pouco comum, comum, muito comum, raro, muito raro.")
    
    data_apresenta = {
        'doença_id': doenca_id,
        'sintoma_id': sintoma_id,
        'frequencia': frequencia
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


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# QUESTÃO 2 #

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
        log_operacao("Listagem de Sintomas", "Usuario vizualizou a lista de sintomas")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        
def lista_patogeno():
    try:
        cursor.execute('SELECT * FROM patogeno;')
        linhas = cursor.fetchall()
        if linhas:
            print("+----+---------------------+---------------------+")
            print("| ID | Patogeno             | Tipo                |")
            print("+----+---------------------+---------------------+")
            for (id, nome, tipo) in linhas:
                print(f"| {str(id).ljust(2)} | {nome.ljust(19)} |  {tipo.ljust(19)} | ")
            print("+----+---------------------+")
        else:
            print("Nenhum patogeno encontrado.")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")

def pesquisar_doenca():
    global arquivos
    arquivos = arquivos +1
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
            
            # ========================= ESCREVER PDF =======================
            pdf_file_path = "relatorioPesquisa" + str(arquivos) + ".pdf"
            c = canvas.Canvas(pdf_file_path, pagesize=letter)
            width, height = letter

            # Define as margens
            left_margin = 50  # Margem esquerda
            top_margin = 50    # Margem superior
            line_height = 15   # Altura entre as linhas

            font_size = 10
            c.setFont("Helvetica", font_size)

            lines = []

            lines.append("+----+---------------------+----------+------------+-----------------------------------------------------------------------------------+")
            lines.append("| ID | Nome Técnico        | CID      | ID Patógeno| Sintomas                                                                          |")
            lines.append("+----+---------------------+----------+------------+-----------------------------------------------------------------------------------+")

            for (id, nome_tecnico, CID, id_patogeno) in r:
                sintomas = listar_sintomas(id)
                lines.append(f"| {str(id).ljust(2)} | {nome_tecnico.ljust(19)} | {CID.ljust(8)} | {str(id_patogeno).ljust(10)} | {sintomas.ljust(44)}                |")

            lines.append("+----+---------------------+----------+------------+-----------------------------------------------------------------------------------+")

            y_position = height - top_margin 

            for line in lines:
                c.drawString(left_margin, y_position, line)
                y_position -= line_height 

            log_operacao("Criacao do relatorio PDF", f"Arquivo: {pdf_file_path}")
            c.save()

        
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

def listar_populares(id):
    try:
        query = ("""
            SELECT GROUP_CONCAT(CONCAT(np.nome)) AS Nome_Popular
            FROM nomes_populares AS np
            WHERE np.`doença_id` = %s;
        """)
        cursor.execute(query, (id,))
        row = cursor.fetchone()

        if row and row[0]:
            return row[0]
        else:
            return "Nenhum nome popular encontrado"

    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return "Erro ao buscar nome popular."

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# QUESTÃO 3 #

def listar_doencas_a_partir_de_uma_lista_de_Sintomas():
    global arquivos2
    arquivos2 = arquivos2 +1
    pdf_file_path = "relatorioListagem" + str(arquivos2) + ".pdf"
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    width, height = letter

    # Define as margens
    left_margin = 50  # Margem esquerda
    top_margin = 20    # Margem superior
    bottom_margin = 20
    line_height = 15   # Altura entre as linhas

    font_size = 10
    c.setFont("Helvetica", font_size)

    lines = []

    numero_sintomas = int(input("Insira quantos sintomas serão: "))
    criterio_sintomas = []

    lines.append(f"Número de sintomas: {numero_sintomas}")
    lines.append("| ============================================================================================ |")

    for i in range(numero_sintomas):
        sintoma = input(f"Insira o nome do sintoma ({i+1}): ")
        lines.append(f"Nome do sintoma ({i+1}): {sintoma}")
        lines.append("| ============================================================================================ |")

        criterio_sintomas.append(sintoma)

    tamanho = len(criterio_sintomas)

    sintomas_str = ', '.join(f"'{sintoma}'" for sintoma in criterio_sintomas)
    
    log_operacao("Busca por Doenças a partir de Sintomas", f"Sintomas fornecidos: {', '.join(criterio_sintomas)}")


    try:
        query = f"""
            SELECT d.id, d.nome_tecnico as Doença, 
                SUM(CASE WHEN s.nome IN ({sintomas_str}) THEN
                    CASE 
                    WHEN a.frequencia = 'muito comum' 	THEN 5
                    WHEN a.frequencia = 'comum' 			THEN 4
                    WHEN a.frequencia = 'pouco comum' 	THEN 3
                    WHEN a.frequencia = 'raro' 			THEN 2
                    WHEN a.frequencia = 'muito raro' 	THEN 1
                    END
                    ELSE 0 
                END) - ({tamanho} - SUM(CASE WHEN s.nome IN ({sintomas_str}) THEN 1 ELSE 0 END)) AS Pesos
                FROM `doença` AS d 
                JOIN apresenta AS a ON a.`doença_id` = d.id
                JOIN sintomas AS s ON a.sintoma_id = s.id
                GROUP BY d.id
                ORDER BY Pesos DESC;
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()

        if not resultados:
            print("Nenhuma doença encontrada com o critério fornecido.")
            lines.append("| ============ Nenhuma doença encontrada! ========== |")
        else:
            print("+----+---------------------+----------+")
            print("| ID | Nome Técnico        | Pesos    |")                                                                     
            print("+----+---------------------+----------+")

            lines.append("+----+---------------------+----------+")
            lines.append("| ID | Nome Técnico        | Pesos    |")                                                                     
            lines.append("+----+---------------------+----------+")

            for (id, Doença, Total) in resultados:
                print(f"| {str(id).ljust(2)} | {Doença.ljust(19)} | {str(Total).ljust(8)} |")
                lines.append(f"| {str(id).ljust(2)} | {Doença.ljust(19)} | {str(Total).ljust(8)} |")
            print("+----+---------------------+----------+")
            lines.append("+----+---------------------+----------+")
            
        log_operacao("Listagem de Doenças", f"Sintomas pesquisados: {', '.join(criterio_sintomas)}")

        escolha_doenca = input(f"A partir da lista, insira o ID da Doença que gostaria de pesquisar: ")
        lines.append("| ============================================================================================ |")
        lines.append(f"ID da Doença pesquisada: {escolha_doenca}")

        try:
            query = f"""
                SELECT d.id, d.nome_tecnico, d.CID, p.nome, p.tipo
                FROM doença AS d
                JOIN patogeno AS p ON d.id_patogeno = p.id
                WHERE d.id = {escolha_doenca};
            """
            cursor.execute(query)
            r = cursor.fetchall()
            if not r:
                print("ID da doença não encontrada.")
                lines.append("| ============ Nenhuma doença encontrada! ========== |")
            else:
                print("+----+---------------------+----------+----------------------------------+-------------------+----------------------------------+")
                print("| ID | Nome Técnico        | CID      | Patógenos                        | Tipo_de_Patogeno  | Nomes_Populares                  |")
                print("+----+---------------------+----------+----------------------------------+-------------------+----------------------------------+")

                lines.append("+----+---------------------+----------+----------------------------------+-------------------+----------------------------------+")
                lines.append("| ID | Nome Técnico        | CID      | Patógenos                        | Tipo_de_Patogeno  | Nomes_Populares                  |")
                lines.append("+----+---------------------+----------+----------------------------------+-------------------+----------------------------------+")

                for (id, nome_tecnico, CID, Patogeno, Tipo_de_Patogeno) in r:
                    nomes_populares = listar_populares(id)
                    sintomas = listar_sintomas(id)
                print(f"| {str(id).ljust(2)} | {nome_tecnico.ljust(19)} | {CID.ljust(8)} | {Patogeno.ljust(32)} |{Tipo_de_Patogeno.ljust(18)} | {nomes_populares.ljust(32)} |")
                print("+----+---------------------+----------+----------------------------------+-------------------+----------------------------------+")
                print("+------------------------------------------------------------------+")
                print("| Sintomas                                                         |")
                print("+------------------------------------------------------------------+")
                print(f"| {sintomas.ljust(64)} |")
                print("+------------------------------------------------------------------+")

                lines.append(f"| {str(id).ljust(2)} | {nome_tecnico.ljust(19)} | {CID.ljust(8)} | {Patogeno.ljust(32)} |{Tipo_de_Patogeno.ljust(18)} | {nomes_populares.ljust(32)} |")
                lines.append("+----+---------------------+----------+----------------------------------+-------------------+----------------------------------+")
                lines.append("+------------------------------------------------------------------+")
                lines.append("| ============================================================================================ |")
                lines.append("| Sintomas                                                         |")
                lines.append(f"| {sintomas.ljust(64)} |")
                lines.append("+------------------------------------------------------------------+")
                
                log_operacao("Pesquisa de Doença", f"ID pesquisado: {escolha_doenca}")

                y_position = height - top_margin 

                for line in lines:
                    if y_position < bottom_margin:
                        c.showPage()
                        y_position = height - top_margin
                        c.setFont("Helvetica", font_size)

                    c.drawString(left_margin, y_position, line)
                    y_position -= line_height 

                log_operacao("Criacao do relatorio PDF", f"Arquivo: {pdf_file_path}")
                c.save()


       
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            log_operacao("Erro ao Buscar Doença", f"Erro: {err}")
            return "Erro ao buscar a doença escolhida."
        
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        log_operacao("Erro ao Buscar Doenças por Sintomas", f"Erro: {err}")
        return "Erro ao buscar sintomas."
    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# MAIN #

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
        print("9. Diagnóstico")
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
        elif escolha == '9':
            listar_doencas_a_partir_de_uma_lista_de_Sintomas()
        elif escolha == '0':
            log_operacao("Saida do sistema")
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()

conexao.close()
cursor.close()
