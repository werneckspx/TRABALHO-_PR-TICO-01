# Bibliotecas 

Para importas as bibliotecas mysql.connector e mysql.connector.errorcode é necessário instalar o mysql-connector-python: 
```
  pip install mysql-connector-python
```

Para importas as bibliotecas reportlab.lib.pagesizes e reportlab.pdfgen é necessário instalar o reportlab:  

```
  pip install reportlab
```
O módulo logging já faz parte da biblioteca padrão do Python, então não é necessário instalar nada adicional.

# Versão 

A verão do Python utilizada foi a 3.12.5.


# Configuração do Banco

Para acessar o banco de dados do MariaDB(HeidiSQL) é necessário que seja trocado os dados de acordo com a sua máquina. No arquivo main.py nas linhas 23 e 24, segue um exemplo da função:

```
  conexao = mysql.connector.connect(host='localhost',
                                    database='doenca',
                                    user=' ',
                                    password=' ')
```













