import Database
from mysql.connector import connect, Error


#Для каждого эксперимента с фигурами создаем отдельную таблицу под названием emulation[i], где i - номер эксперимента.
#Таким образом формируем набор таблиц для дальнейшего анализа.
#Структура таблиц следующая: 1я ячейка - уникальный автозаполняющийся ID
#                            2я ячейка - максимальная/минимальная высота в конкретной итерации
#                            3я ячейка - формы
#                            4я ячейка - позиции форм

new_count_table = 0
table_name = 'location' + str(new_count_table)




def db_create():
    try:
        with connect(
                host=Database.db_host_name,
                user=Database.db_user_name,
                password=Database.db_password,
        ) as connection:
            create_db_query = f"CREATE DATABASE {Database.db_name}"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
        print("Соединение с MySQL открыто")
    except Error as e:
        print(e)
    finally:
        # Если соединение было установлено
        if connection:
            # Закрываем курсор
            cursor.close()
            # Закрываем соединение
            connection.close()
            print("Соединение с MySQL закрыто")


def create_tables(table_name):
    try:
        # Подключение к существующей базе данных
        Database.connection = connect(host=Database.db_host_name,
                                      user=Database.db_user_name,
                                      password=Database.db_password,
                                      database=Database.db_name)
        Database.cursor = Database.connection.cursor()
        sql_create_tables = f"""CREATE TABLE {table_name}(
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            height FLOAT,
                            shapes VARCHAR(100),
                            positions VARCHAR(100));"""
        # Выполняем sql запросы на создание таблицы
        print("Соединение с MySQL открыто")
        Database.cursor.execute(sql_create_tables)
        Database.connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с MySQL", error)
    finally:
        if Database.connection:
            Database.cursor.close()
            Database.connection.close()
            print("Соединение с MySQL закрыто")


def drop_tables(table_name):
    try:
        # Подключение к существующей базе данных
        Database.connection = connect(host=Database.db_host_name,
                                      user=Database.db_user_name,
                                      password=Database.db_password,
                                      database=Database.db_name)
        Database.cursor = Database.connection.cursor()
        print("Соединение с MySQL открыто")

        #Удаляем censors
        sql_drop_tables = f'drop table {table_name};'
        Database.cursor.execute(sql_drop_tables)
        Database.connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с MySQL", error)
    finally:
        if Database.connection:
            Database.cursor.close()
            Database.connection.close()
            print("Соединение с MySQL закрыто")

