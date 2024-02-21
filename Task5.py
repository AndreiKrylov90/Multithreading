# Создать программу, которая будет производить подсчет количества слов в
# каждом файле в указанной директории и выводить результаты в консоль.
# �спользуйте процессы.

from pathlib import Path
import time
import multiprocessing


def count_words(file: Path, start_time):
    with open(file, encoding='utf-8') as f:
        text = f.read()
    print(f"In file {file.name} {len(text.split())} words - {time.time() - start_time} ")

def counting_words_in_directory(path: Path):
    start_time = time.time()
    files = [file for file in path.iterdir() if file.is_file()]
    processes = []
    for file in files:
        process = multiprocessing.Process(target=count_words, args=[file, start_time])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()



if __name__ == '__main__':
    path = Path(Path.cwd() / 'upload')
    counting_words_in_directory(path)

