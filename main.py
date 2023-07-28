import uvicorn as uvicorn
from fastapi import security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from utils import Transaction, config, execute_query
from fastapi import FastAPI, Security


app = FastAPI()
API_TOKEN = config(section='host_info').get('API_TOKEN')


@app.post("/transactions")
async def create_transaction(transaction: Transaction, credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Эндпоинт для создания новой транзакции
    :param transaction: Информация о транзакции
    :param credentials: Ключ к апи
    :return: Уведомляем об успехе/неуспехе записи
    """

    # Проверка токена
    received_token = credentials.credentials
    if received_token != API_TOKEN:
        raise HTTPException(status_code=401)

    message = "Transaction created successfully"
    try:
        sql = "INSERT INTO transactions (transactionsId, amount, type) VALUES ({}, {}, {})".format(
            transaction.id, transaction.amount, transaction.type
        )
        insert_to_sql = execute_query(sql)
        if insert_to_sql != 'no results for fetch':
            message = insert_to_sql
    except Exception as E:
        message = E
    finally:
        return JSONResponse({"status": message})


@app.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: int, credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Эндпоинт для получения информации о транзакции по идентификатору
    :param transaction_id: айди транзакции
    :param credentials: Ключ к апи
    :return: словарь, содержащий amount, type
    """

    # Проверка токена
    received_token = credentials.credentials
    if received_token != API_TOKEN:
        raise HTTPException(status_code=401)

    transaction_data = {"msg": False}
    try:
        sql = 'SELECT amount, type FROM transactions WHERE transactionsId = {};'.format(transaction_id)
        transaction_info = execute_query(sql)  # При SELECT запросах приходит кортеж в стиле [(100, 100)]

        if len(transaction_info) > 0:  # есть ли такая транзакция в БД
            amount = transaction_info[0][0]
            transaction_type = transaction_info[0][1]

            transaction_data = {
                "amount": amount,
                "type": transaction_type
            }
    except Exception as E:
        transaction_data = {"msg": E}
    finally:
        return JSONResponse(transaction_data)


if __name__ == '__main__':
    HOST_IP = config(section='host_info').get('HOST_IP')
    uvicorn.run("main:app", host=HOST_IP, port=8000)
