from getpass import getpass
from mysql.connector import connect, Error
import configparser


config = configparser.ConfigParser()
config.read("DBSettings.ini")
db_name = config["Database"]["db_name"]
db_password = config["Database"]["db_password"]
db_user_name = config["Database"]["db_user_name"]
db_host_name = config["Database"]["db_host_name"]
db_charset = config["Database"]["db_charset"]


#Объект соединения с базой данных
connection = None

#Курсор в SQL – это область в памяти базы данных, которая предназначена для хранения последнего оператора SQL.
# Если текущий оператор – запрос к базе данных, в памяти сохраняется и строка данных запроса,
# называемая текущим значением, или текущей строкой курсора.
cursor = None


def open_db_connection():
    global connection, cursor
    try:
        connection = connect(
                host=db_host_name,
                user=db_user_name,
                password=db_password,
                database=db_name)
        cursor = connection.cursor()
        print("Соединение с MySQL открыто")
    except Error as e:
        print(e)
    return connection, cursor


def close_db_connection():
    global connection, cursor
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с MySQL закрыто")


def write_one_row_in_db(table_name, height, shapes, positions):
    global connection, cursor
    rw = 0
    try:
        sql_insert = f"INSERT INTO emulation.{table_name} ("\
                            "height,"\
                            "shapes,"\
                            "positions"\
                            ") VALUES (%s,%s,%s);"

        cursor.execute(sql_insert, (height, shapes, positions))
        connection.commit()
        rw = 1
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        connection.rollback()
    return rw

def get_string(table_name, id):
    global connection, cursor
    try:
        mysql_string = f"SELECT * FROM {table_name}" + " WHERE id = {!s}".format(id)
        cursor.execute(mysql_string)
        result = cursor.fetchall()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        connection.rollback()
    return result

new_count_table = 0
table_name = 'emulation' + str(new_count_table)
