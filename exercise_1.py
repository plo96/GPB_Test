"""# == == == == == == == == == == == == == == == == == == == == == == №1
# имеется текстовый файл file.csv, в котром разделитель полей с данными: | (верт. черта)
# пример ниже содержит небольшую часть этого файла(начальные 3 строки, включая строку заголовков полей)

\"""
lastname|name|patronymic|date_of_birth|id
Фамилия1|Имя1|Отчество1 |21.11.1998   |312040348-3048
Фамилия2|Имя2|Отчество2 |11.01.1972   |457865234-3431
...
\"""

# Задание
# 1. Реализовать сбор уникальных записей
# 2. Случается, что под одиннаковым id присутствуют разные данные - собрать отдельно такие записи"""
from dataclasses import dataclass


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


def main():
    filename = 'file.csv'
    with open(filename, mode='r', encoding='windows-1251') as file:
        all_strings = file.readlines()  # считываем все данные с файла по строкам

    dict_of_unique_records: dict[str: Record] = {}
    dict_of_not_unique_records: dict[str: list[Record]] = {}

    for string in all_strings[1:]:  # перебираем все строки с записями (игнорируем заголовки)

        string = string.rstrip('\n')  # 'чистим' строку от знака переноса строки если надо
        record = string.split('|')  # раздиляем строку на поля
        record = [field.strip(' ') for field in record]  # 'чистим' строки от пробелов

        record = Record(*record)  # Переводим запись в экземпляр Record

        if record.id in dict_of_not_unique_records:
            dict_of_not_unique_records[record.id].append(record)
            continue

        if record.id in dict_of_unique_records:
            dict_of_not_unique_records[record.id] = list((dict_of_unique_records[record.id], record))
            continue

        dict_of_unique_records[record.id] = record

    print(dict_of_unique_records)  # Все ПОЛНОСТЬЮ уникальные записи
    print(dict_of_not_unique_records)  # Все записи у которых одинаковый id


if __name__ == '__main__':
    main()
