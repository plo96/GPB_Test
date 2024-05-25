"""============================================ №4
# Имеется папка с файлами
# Реализовать удаление файлов старше N дней"""

from datetime import datetime
from pathlib import Path


def removing_old_files(path: Path, N: int):
    """
    Функция для удаления файлов старше указанного количества дней.
    :param path: Путь для удаления файлов.
    :param N: Количество дней.
    :return: None.
    """
    time_now = datetime.now().date()
    for file in path.iterdir():
        file_created = datetime.fromtimestamp(file.stat().st_ctime).date()
        if (time_now - file_created).days > N:
            file.unlink()


def main():
    path = 'example_dir'
    N = 10
    path = Path.cwd() / path
    removing_old_files(path=path, N=N)


if __name__ == "__main__":
    main()
