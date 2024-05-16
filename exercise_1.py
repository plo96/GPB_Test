# == == == == == == == == == == == == == == == == == == == == == == №1
# # имеется текстовый файл file.csv, в котром разделитель полей с данными: | (верт. черта)
# # пример ниже содержит небольшую часть этого файла(начальные 3 строки, включая строку заголовков полей)
#
# """
# lastname|name|patronymic|date_of_birth|id
# Фамилия1|Имя1|Отчество1 |21.11.1998   |312040348-3048
# Фамилия2|Имя2|Отчество2 |11.01.1972   |457865234-3431
# ...
# """
#
# # Задание
# # 1. Реализовать сбор уникальных записей
# # 2. Случается, что под одиннаковым id присутствуют разные данные - собрать отдельно такие записи
from dataclasses import dataclass


def delete_empty_strings(some_list: list[str]) -> list:
	"""Возвращет список, идентичный текущему, но без пустых строк в значениях."""
	clear_list: list = []
	for value in some_list:
		if value != '':
			clear_list.append(value)
	return clear_list


@dataclass
class Record:
	"""Класс для сбора записей."""
	lastname: str
	name: str
	patronymic: str
	date_of_birth: str
	id: str
	
	def __hash__(self):
		return hash(tuple(self.__getattribute__(attr_name) for attr_name in self.__annotations__.keys()))


@dataclass
class MultiRecordId:
	"""Класс для сбора разных записей под одинаковым id."""
	id: str
	records: list[Record]


def main():
	filename = 'file.csv'
	with open(filename, mode='r') as file:
		
		all_data = file.read()  						 	 # считываем все данные с файла
	
	all_strings = all_data.split('\n') 						 # разделяем строки
	
	all_strings = delete_empty_strings(all_strings) 		 # удаляем пустые строки
	
	list_of_records: list[Record] = []
	for string in all_strings[1:]: 							 # перебираем все строки с записями (игнорируем заголовки)
		record = string.split('|') 							 # раздиляем строку на поля
		record = [field.strip(' ') for field in record] 	 # 'чистим' строки от пробелов
		list_of_records.append(Record(*record)) 			 # Переводим все записи в экземпляры Record
	
	list_of_unique_records = list(set(list_of_records)) 	 # ОТВЕТ: уникальные записи
	print(f'{list_of_unique_records=}')
	
	dict_of_id_records: dict[str: list[Record]] = {} 		 # Словарь вида {'id': list['not_unique_record_1', ...]}
	for record in list_of_unique_records:  					 # Агрегируем к каждому id список привязанных записей
		if record.id in dict_of_id_records.keys():
			dict_of_id_records[record.id].append(record)
		else:
			dict_of_id_records[record.id] = [record]
	
	list_of_multi_record_id: list = []
	for record_id, records in dict_of_id_records.items():	# Отбираем id с несколькими записями
		if len(records) > 1:
			multi_record_id = MultiRecordId(id=record_id, records=records)
			list_of_multi_record_id.append(multi_record_id)
	
	print(list_of_multi_record_id)  						# ОТВЕТ: id, которым соответствуют множество записей.


if __name__ == '__main__':
	main()
