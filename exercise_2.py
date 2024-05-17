"""== == == == == == == == == == == == == == == == == == == == == == №2
# в наличии список множеств. внутри множества целые числа
m = [{11, 3, 5}, {2, 17, 87, 32}, {4, 44}, {24, 11, 9, 7, 8}]

# Задание: посчитать
#  1. общее количество чисел
#  2. общую сумму чисел
#  3. посчитать среднее значение
#  4. собрать все множества в один кортеж
# *написать решения в одну строку"""
from functools import reduce


def main():
	m = [{11, 3, 5}, {2, 17, 87, 32}, {4, 44}, {24, 11, 9, 7, 8}]
	
	sum_length = sum(len(s) for s in m)			# ОТВЕТ: Общее количество чисел
	print(sum_length)
	
	sum_of_nums = sum(sum(s) for s in m)  		# ОТВЕТ: Общая сумма чисел
	print(sum_of_nums)
	
	avr_of_nums = sum(sum(s) for s in m) / sum(len(s) for s in m)	# ОТВЕТ: Среднее значение (sum_of_nums / sum_length)
	print(avr_of_nums)

	sum_tuple = reduce(lambda x, y: x + y, (tuple(s) for s in m))	# ОТВЕТ: Один кортеж из всех чисел
	print(sum_tuple)


if __name__ == "__main__":
	main()
