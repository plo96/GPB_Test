# ============================================ №4
# # Имеется папка с файлами
# # Реализовать удаление файлов старше N дней

import os

dir_name = 'example_dir'

os.chdir(dir_name)

with open('file_1', mode='r') as file:
	os.fdatasync(file)

