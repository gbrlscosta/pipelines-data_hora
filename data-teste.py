from openpyxl import load_workbook
import pandas as pd
from datetime import datetime
import psycopg2

try:
    connection = psycopg2.connect(
        host='devops-postgresql-pipeline-banco-postgresql-devops.e.aivencloud.com',
        user='avnadmin',
        password='AVNS_soL4IKAZqbRQwbx06Jb',
        database='dbdatahora',
        port='24043'
    )

    cursor = connection.cursor()
    cursor.execute("SELECT current_database();")
    database_name = cursor.fetchone()
    print("Conectado ao banco de dados:", database_name)
    
    select_query = f"SELECT * FROM data;"

    cursor.execute(select_query)

    registros = cursor.fetchall()

    colunas = [desc[0] for desc in cursor.description]

    dados = pd.DataFrame(registros, columns=colunas)

    data_atual = datetime.now().strftime("%Y-%m-%d")
    hora_atual = datetime.now().strftime("%H:%M:%S")
    
    codigo = dados['codigo'].max() + 1

    novo_dado_excel = pd.DataFrame({"codigo": [codigo], "data": [data_atual], "hora": [hora_atual]})
    dados = pd.concat([dados, novo_dado_excel], ignore_index=True)

    dados.to_excel("data_hora.xlsx", index=False)

    insert_query = """
    INSERT INTO data (codigo, data, hora)
    VALUES (%s, %s, %s);
    """
    valores = (int(codigo), data_atual, hora_atual)

    cursor.execute(insert_query, valores)
    connection.commit()

    print("SOMENTE TESTANDO RSRSRS")
    
except (Exception, psycopg2.Error) as error:
    print("Erro ao inserir dados:", error)

finally:
    if connection:
        cursor.close()
        connection.close()
        print("Conexão com PostgreSQL fechada")
