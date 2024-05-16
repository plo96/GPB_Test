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

import requests as req
from pydantic import BaseModel
from pandas import DataFrame


class Response(BaseModel):
	Columns: list[str]
	Description: str
	RowCount: int
	Rows: list[list[int, datetime, str]]\
	

def main():
	documents_date = datetime.fromisoformat(date.today().isoformat()).timestamp()
	response = req.get(url=f'https://api.gazprombank.ru/very/important/docs?documents_date={documents_date}')
	
	# Мапимся на модель, валидируя ВСЕ данные ответа. Не понял из ТЗ, мапить всё или только важные данные.
	response = Response.model_validate_json(response.json())
	
	important_data = DataFrame(
		document_id=[response.Rows[i][0] for i in range(len(response.Rows))],
		document_dt=[response.Rows[i][1] for i in range(len(response.Rows))],
		document_name=[response.Rows[i][2] for i in range(len(response.Rows))],
	)
	
	important_data.update(load_dt=datetime.now())
	
	
if __name__ == "__main__":
	main()
