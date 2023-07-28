from configparser import ConfigParser
from pydantic import BaseModel
import psycopg2
from configparser import ConfigParser


class Transaction(BaseModel):
    # Понимаю что стоило убрать класс валидации в отдельный файл но в рамках тестового,
    # думаю можно держать все инструменты в одном файле, учитывая, что сервис небольшой :)
    id: int
    amount: float
    type: str


def config(filename='config.ini', section='postgresql'):
    """
    Функция выгрузки данных из файла-конфига, выгружает словарь со всем содержимым
    """
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


def execute_query(sql_query):
    """
    Функция принимает выражение, подключается к БД и применяет его к postgres
    """
    conn = None
    response = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql_query)

        response = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return ""
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')
            if response is not None:
                return response
            else:
                return ""


