# ============================================ №6*
# Имеется банковское API возвращающее JSON
# {
# 	"Columns": ["key1", "key2", "key3"],
# 	"Description": "Банковское API каких-то важных документов",
# 	"RowCount": 2,
# 	"Rows": [
# 		["value1", "value2", "value3"],
# 		["value4", "value5", "value6"]
# 	]
# }
# Основной интерес представляют значения полей "Columns" и "Rows",
# которые соответственно являются списком названий столбцов и значениями столбцов
#
# Задание:
# 	1. Получить JSON из внешнего API
# 		ендпоинт: GET https://api.gazprombank.ru/very/important/docs?documents_date={"начало дня сегодня в виде таймстемп"}
# 	2. Валидировать входящий JSON используя модель pydantic
# 		(из ТЗ известно что поле "key1" имеет тип int, "key2"(datetime), "key3"(str))
# 	2. Представить данные "Columns" и "Rows" в виде плоского csv-подобного pandas.DataFrame
# 	3. В полученном DataFrame произвести переименование полей по след. маппингу
# 		"key1" -> "document_id", "key2" -> "document_dt", "key3" -> "document_name"
# 	3. Полученный DataFrame обогатить доп. столбцом:
# 		"load_dt" -> значение "сейчас"(датавремя)
from datetime import datetime, date
from typing import Union

import requests as req
from pydantic import BaseModel
from pandas import DataFrame


class Response(BaseModel):
    Columns: list[str]
    Description: str
    RowCount: int
    Rows: list[list[Union[int, datetime, str]]]


# Из условия я понял что надо валидировать значение не полей 'key' из Column, а соответствующие им поля в Rows (т.к.)/
# в строках храняться сами данные, а в Columns - ключи.
# В отдельную функцию вынес валидацию данных в каждой строке, т.к. с помощью аннотации типов,
# которую воспринимает pydantic, смог задать только ограничения на тип данных во ВСЕХ ячейках списка сразу.
def parse_row(row: list) -> list[Union[int, datetime, str]]:
    try:
        field_1 = int(row[0])
    except ValueError:
        raise ValueError('error in rows validation. row[0] must be int.')

    try:
        field_2 = datetime.fromisoformat(row[1])
    except ValueError:
        raise ValueError('error in rows validation. row[1] must be datetime.')

    try:
        field_3 = str(row[2])
    except ValueError:
        raise ValueError('error in rows validation. row[2] must be str.')

    return [field_1, field_2, field_3]


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
    # Мапимся на модель, валидируя ВСЕ данные ответа. Не понял из ТЗ, мапить всё или только важные данные.
    response = Response(Rows=[parse_row(row) for row in response.pop("Rows")], **response)	# ОТВЕТ: валидация данных

    print(response)

    important_data = DataFrame(response.Rows, columns=response.Columns)			# ОТВЕТ: представление в виде DataFrame

    important_data.columns = ['document_id', 'document_dt', 'document_name']	# ОТВЕТ: переименование columns

    important_data['load_dt'] = [datetime.now() for _ in range(len(response.Rows))]

    print(important_data)					# ОТВЕТ: дополненный DataFrame


if __name__ == "__main__":
    main()
