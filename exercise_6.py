"""============================================ №6*
Имеется банковское API возвращающее JSON
{
    "Columns": ["key1", "key2", "key3"],
    "Description": "Банковское API каких-то важных документов",
    "RowCount": 2,
    "Rows": [
        ["value1", "value2", "value3"],
        ["value4", "value5", "value6"]
    ]
}
Основной интерес представляют значения полей "Columns" и "Rows",
которые соответственно являются списком названий столбцов и значениями столбцов

Задание:
    1. Получить JSON из внешнего API
        ендпоинт: GET https://api.gazprombank.ru/very/important/docs?documents_date={"начало дня сегодня в виде таймстемп"}
    2. Валидировать входящий JSON используя модель pydantic
        (из ТЗ известно что поле "key1" имеет тип int, "key2"(datetime), "key3"(str))
    2. Представить данные "Columns" и "Rows" в виде плоского csv-подобного pandas.DataFrame
    3. В полученном DataFrame произвести переименование полей по след. маппингу
        "key1" -> "document_id", "key2" -> "document_dt", "key3" -> "document_name"
    3. Полученный DataFrame обогатить доп. столбцом:
        "load_dt" -> значение "сейчас"(датавремя)"""
from datetime import datetime, date
from typing import Union

import requests as req
from pydantic import BaseModel
from pandas import DataFrame


class Row(BaseModel):
    key1: int
    key2: datetime
    key3: str


class Response(BaseModel):
    Columns: list[str]
    Description: str
    RowCount: int
    Rows: list[Row]


def main():
    documents_date = datetime.fromisoformat(date.today().isoformat()).timestamp()
    # Не могу получить данные по этому url, он точно рабочий? Какими только способами не пытался...
    # Продолжаю, считая что получил.
    # response = req.get(url=f'https://api.gazprombank.ru/very/important/docs?documents_date={documents_date}')
    # response = response.json()			# ОТВЕТ: полечение данных в запросе

    # Замокал ответ вручную :)
    response = {
        "Columns": ["key1", "key2", "key3"],
        "Description": "Банковское API каких-то важных документов",
        "RowCount": 2,
        "Rows": [
            [123, "2024-05-24", "value3"],
            [456, "2024-05-24", "value6"]
        ]
    }

    # Приводим список Rows в response, содержащий списки со значениями, к словарю, чтобы можно было валидировать через pydantic
    rows_dicts: list[dict] = []
    for row in response.pop("Rows"):
        row_dict = {response["Columns"][i]: row[i] for i in range(len(response["Columns"]))}
        rows_dicts.append(row_dict)
    response["Rows"] = rows_dicts

    # Мапимся на модель, валидируя ВСЕ данные ответа. Не понял из ТЗ, мапить всё или только важные данные.
    response = Response(**response)             # ОТВЕТ: валидация данных

    important_data = DataFrame(response.Rows, columns=response.Columns)  # ОТВЕТ: представление в виде DataFrame

    important_data.columns = ['document_id', 'document_dt', 'document_name']  # ОТВЕТ: переименование columns

    important_data['load_dt'] = [datetime.now() for _ in range(len(response.Rows))]

    print(important_data)  # ОТВЕТ: дополненный DataFrame


if __name__ == "__main__":
    main()
