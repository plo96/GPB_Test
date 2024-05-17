"""============================================ №4
# Имеется папка с файлами
# Реализовать удаление файлов старше N дней"""

import os
from datetime import datetime
from pathlib import Path


def removing_old_files(path: str | Path, N: int):
    """
    Функция для удаления файлов старше указанного количества дней.
    :param path: Путь для удаления файлов.
    :param N: Количество дней.
    :return: None.
    """
    time_now = datetime.now().date()
    os.chdir(path)
    for file in os.listdir():
        file_created = datetime.fromtimestamp(os.path.getctime(file)).date()
        if (time_now - file_created).days > N:
            os.remove(file)

    os.chdir(Path(__file__).parent)				# Возвращение в родную директорию файла (на всякий случай)


def main():
    path = 'example_dir'
    N = 10
    removing_old_files(path=path, N=N)


if __name__ == "__main__":
    main()
