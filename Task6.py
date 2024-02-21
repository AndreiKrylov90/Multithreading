# Создать программу, которая будет производить подсчет количества слов в
# каждом файле в указанной директории и выводить результаты в консоль.
# �спользуйте асинхронный подход.


from pathlib import Path
import time
import asyncio


async def count_words_async(file: Path, start_time):
    with open(file, encoding='utf-8') as f:
        text = f.read()
    print(f"In file {file.name} {len(text.split())} words - {time.time() - start_time} ")


async def counting_words_in_directory_async(path: Path):
    start_time = time.time()
    files = [file for file in path.iterdir() if file.is_file()]
    tasks = []
    for file in files:
        task = count_words_async(file, start_time)
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    path = Path(Path.cwd() / 'upload')
    asyncio.run(counting_words_in_directory_async(path))

