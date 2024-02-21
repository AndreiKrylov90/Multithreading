# Напишите программу на Python, которая будет находить сумму элементов массива из 1000000 целых чисел.
# �ример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# �ассив должен быть заполнен случайными целыми числами от 1 до 100.
# �ри решении задачи нужно использовать многопоточность, многопроцессорность и асинхронность.
# � каждом решении нужно вывести время выполнения вычислений.

from random import randint
import time
import asyncio
import threading
from multiprocessing import Process, Value, Lock


def generate_random_numbers():
    arr = []
    for i in range(10000000):
        number = randint(1, 100)
        arr.append(number)
    return arr


def counting_sum_sync(arr: list):
    start_time = time.time()
    sum = 0
    for i in arr:
        sum += i
    print(f'Sync: sum of all elements in list is {sum} in {time.time() - start_time:.2f} seconds')


def counting_sum_in_treads(arr: list, start_time, thread_id, result, lock):
    sum = 0
    for i in arr:
        sum += i
    with lock:
        result[thread_id - 1] = sum


def counting_sum_thread(arr: list, attempts: int):
    start_time = time.time()
    num_threads = attempts
    chunk_size = len(arr) // num_threads
    result = [0] * num_threads
    lock = threading.Lock()

    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size if i < num_threads - 1 else len(arr)
        thread = threading.Thread(target=counting_sum_in_treads, args=(arr[start:end], start_time, i+1, result, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(result)
    print(f'Threads: sum of all elements in list is {total_sum} in {time.time() - start_time:.2f} seconds')


def counting_sum_in_process(arr, start_time, process_id, result, lock):
    sum = 0
    for i in arr:
        sum += i
    with lock:
        result.value += sum


def counting_sum_process(arr: list, attempts: int):
    start_time = time.time()
    num_processes = attempts
    chunk_size = len(arr) // num_processes
    result = Value('i', 0)
    lock = Lock()

    processes = []
    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(arr)
        process = Process(target=counting_sum_in_process, args=(arr[start:end], start_time, i+1, result, lock))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    total_sum = result.value
    print(f'Processes: sum of all elements in list is {total_sum} in {time.time() - start_time:.2f} seconds')


async def generate_random_numbers_async(n):
    arr = []
    for i in range(n):
        number = randint(1, 100)
        arr.append(number)
    return arr


async def counting_sum_in_async(arr, start_time):
    sum = 0
    for i in arr:
        sum += i
    return sum

async def counting_sum_async(arr: list, attempts: int):
    start_time = time.time()
    num_processes = attempts
    chunk_size = len(arr) // num_processes

    tasks = []
    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i < num_processes - 1 else len(arr)
        task = asyncio.create_task(counting_sum_in_async(arr[start:end], start_time))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    print(f'Async: sum of all elements in list is {total_sum} in {time.time() - start_time:.2f} seconds')


if __name__ == '__main__':
    arr = generate_random_numbers()
    attempts = 100
    counting_sum_sync(arr)
    counting_sum_thread(arr, attempts)
    counting_sum_process(arr, attempts)
    asyncio.run(counting_sum_async(arr, attempts))
