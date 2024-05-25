"""============================================ №5*
В наличии текстовый файл с набором русских слов(имена существительные, им.падеж)
Одна строка файла содержит одно слово.

Задание:
Написать программу которая выводит список слов,
каждый элемент списка которого - это новое слово,
которое состоит из двух сцепленных в одно, которые имеются в текстовом файле.
Порядок вывода слов НЕ имеет значения

Например, текстовый файл содержит слова:
ласты
стык
стыковка
баласт
кабала
карась

Пользователь вводмт первое слово: ласты
Программа выводит:
ластык
ластыковка

Пользователь вводмт первое слово: кабала
Программа выводит:
кабаласты
кабаласт

Пользователь вводмт первое слово: стыковка
Программа выводит:
стыковкабала
стыковкарась
"""

def get_similar_letter_number(first_word: str, second_word: str) -> int:
	"""Возвращает число общих букв в конце первого слова и в начале второго."""
	min_word_length = min(len(first_word), len(second_word))
	for word_part_size in range(min_word_length, 0, -1):
		if first_word.endswith(second_word[:word_part_size]):
			return word_part_size
	return 0


def get_double_words(file_name: str, first_word: str) -> list[str] | None:
	"""Функция, которая делает то, что требуется в условии."""
	with open(file_name, mode='r', encoding='UTF-8') as file:
		words: list = file.read().split('\n')
	
	if first_word not in words:
		print("""В условии сказано что составные слова должны состоять из двух сцепленных слов,
				 КОТОРЫЕ ИМЕЮСТЯ В ТЕКСТОВОМ ФАЙЛЕ.
				 Поэтому работать программа не будет, если введенного первого слова нет в текстовом файле.
				 (на самом деле будет, просто уберите этот 'if')""")
		return
	
	answer: list = []
	for word in words:
		if first_word == word:				# два одинаковых слова не дают новое, хотя и имеют общие буквы
			continue
		similar_letter_number = get_similar_letter_number(first_word, word)
		if similar_letter_number > 0:
			answer.append(f'{first_word[:-similar_letter_number]}{word}')
	
	for word in answer:
		print(word)
	print('\n')
	
	return answer  # ОТВЕТ


def main():
	file_name = 'words_list.txt'
	# Проверка написанной функции на примерах из описания. Также в неё добавлен print, т.к. вывод текста был в условии.
	assert get_double_words(
		file_name=file_name,
		first_word='ласты',
	) == ['ластык', 'ластыковка']
	
	assert get_double_words(
		file_name=file_name,
		first_word='кабала',
	) == ['кабаласты', 'кабаласт']
	
	assert get_double_words(
		file_name=file_name,
		first_word='стыковка',
	) == ['стыковкабала', 'стыковкарась']


if __name__ == "__main__":
	main()
