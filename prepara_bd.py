import mysql.connector
from mysql.connector import errorcode

# realiza a conexão com o banco de dados
print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

cursor = conn.cursor()

# deleta, cria e coloca em uso o banco de dados da aplicação
cursor.execute("DROP DATABASE IF EXISTS `smart_fi`;")
cursor.execute("CREATE DATABASE `smart_fi`;")
cursor.execute("USE `smart_fi`;")

# cria as tabelas do banco de dados
TABLES = {}

TABLES['user'] = (
    '''
    CREATE TABLE `user` (
    `user_id`       INT(11)         NOT NULL AUTO_INCREMENT,
    `email`         VARCHAR(50)     NOT NULL,
    `name`          VARCHAR(50)     NOT NULL,
    `birthdate`     DATE            NOT NULL,
    `password`      VARCHAR(100)    NOT NULL,
    PRIMARY KEY (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    '''
)

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end=' ')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

# insere usuarios no banco de dados
usuario_sql = 'INSERT INTO user (email, name, birthdate, password) VALUES (%s, %s, %s, %s)'
usuarios = [
    ("diego@example.com", "Diego Paraguai", "1996-11-19", "senha123"),
    ("rodrigo@example.com", "Rodrigo Ribeiro", "1997-06-14", "senha456")]

cursor.executemany(usuario_sql, usuarios)

# executa query no banco de dados e imprime no terminal
cursor.execute('select * from `smart_fi`.user')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(f'email: {user[1].ljust(50)} nome: {user[2]}')

# commita se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
