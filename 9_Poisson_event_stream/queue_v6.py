import datetime
from datetime import time
from math import log
from random import random


def my_print(time, hairdresser, queue):
    current_time = str(time)
    current_time = ':'.join(str(current_time).split(':')[:2])
    print(f'{current_time}\t', end=' ')
    for _ in range(len(hairdresser)):
        print(hairdresser[_], end=' ')
    print(f'/ {queue}')


# Генерируем длительность ожидания новых заявок
def generate_x(lambd):
    x = random()
    time_x = - (1 / lambd) * (log(x))
    return time_x


# Генерируем время работы парикмахера
def generate_y(mu):
    y = random()
    time_y = - (1 / mu) * (log(y))
    return time_y


# Рассаживаем клиентов по креслам
def services(i, list_mu, hours_start, minutes_start, current_time, queue):
    list_hairdresser[i] = 1
    time_of_event = int(minutes_start + generate_y(list_mu[i]))
    if time_of_event >= 60:
        hours_start = hours_start + time_of_event // 60
        minutes_start = minutes_start % 60
        time_of_service = time(hours_start, minutes_start)
        dict_time_of_service[j + 1] = time_of_service
    else:
        time_of_service = time(hours_start, time_of_event)
        dict_time_of_service[i + 1] = time_of_service
    if comment == 1:
        print(f'Стрижка началась у {i + 1} парикмахера')
        if queue > 0:  # освобождаем очередь
            queue -= 1
        my_print(time=current_time, hairdresser=list_hairdresser, queue=queue)


try:
    n = int(input('Введите количество парикмахеров: '))
except ValueError:
    print('Что-то пошло не так')

list_mu = []
list_hairdresser = []
for i, j in enumerate(range(n)):
    try:
        mu = float(input(f'Введите интенсивность обслуживания {i + 1} парикмахера: '))
        list_mu.append(mu)
        list_hairdresser.append(j + 1)
    except ValueError:
        print('Что-то пошло не так')

try:
    lambd = float(input('Введите интенсивность потока клиентов, желающих подстричься: '))
except ValueError:
    print('Что-то пошло не так')

comment = int(input('Введите цифру 1 если хотите видеть комментарии или 0: '))

hours_start = 10
minutes_start = 00
hours_finish = 20
minutes_finish = 00

time_start = time(hours_start, minutes_start)
time_end = time(hours_finish, minutes_finish)
current_time = time_start

dict_time_of_service = {}  # Храним в словаре время окончания работы каждого парикмахера
queue = 0  # Храним очередь в парикмахерскую

# Выставляем по умолчанию парикмахеров свободными
for i in range(len(list_hairdresser)):
    list_hairdresser[i] = 0

# Открываем парикмахерскую, пока время работы не истекло :)
my_print(time=current_time, hairdresser=list_hairdresser, queue=queue)

while current_time < time_end:
    for j in range(len(list_hairdresser)):
        # Генерируем событие (приход клиента)
        minutes_start = int(minutes_start + generate_x(lambd))
        if minutes_start >= 60:
            hours_start = hours_start + minutes_start // 60
            minutes_start = minutes_start % 60
            current_time = time(hours_start, minutes_start)
        else:
            current_time = time(hours_start, minutes_start)

        if list_hairdresser[j] == 0:
            services(j, list_mu, hours_start, minutes_start, current_time, queue)
            break

        # Проверяем словарь с временем работы каждого парикмахера, если время работы парикмахера истекло, то \
        # освобождаем кресло, садим другого клиента и уменьшаем очередь
        for key in dict_time_of_service:
            time_key = dict_time_of_service.get(key)
            if time_key < current_time:
                if comment == 1:
                    print(f'Стрижка закончена у {key} парикмахера')
                list_hairdresser[key - 1] = 0  # освобождаем кресло
                # if queue > 0:  # освобождаем очередь
                #     queue -= 1
                my_print(time=time_key, hairdresser=list_hairdresser, queue=queue)
        chair = 0
        for k in range(len(list_hairdresser)):
            if list_hairdresser[k] == 0:
                # Усаживаем клиента за свободное кресло
                services(k, list_mu, hours_start, minutes_start, current_time, queue)
            else:
                chair += 1
        if chair == len(list_hairdresser):
            queue += 1
            if comment == 1:
                print('Все парикмахеры заняты. Садим клиента в очередь :(')
            my_print(time=current_time, hairdresser=list_hairdresser, queue=queue)
