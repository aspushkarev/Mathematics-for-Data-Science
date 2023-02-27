# Напишите программу,вычисляющую по заданной таблице сопряжённости признаков
# – статистику хи-квадрат,
# – P-значение для критерия хи-квадрат Фишера-Пирсона,
# – нормированные коэффициенты связи, основанные на статистике хи-квадрат,
# – меры прогнозы Гутмана,
# – коэффициенты контингенции и ассоциации (если таблица имеет размер 2 × 2)
import numpy as np
import scipy.stats
from scipy.stats import chi2


def dependency_research():
    # Создадим матрицу сопряжённости
    size = int(input('Введите количество строк таблицы сопряженности: '))

    # Запросим значения строк матрицы
    cont_list = []
    for i, j in enumerate(range(size)):
        a = list(map(int, input(f'Введите значения {i + 1} строки таблицы сопряженности через пробел: ').split()))
        sum_a = sum(a)
        a.append(sum_a)
        cont_list.append(a)

    contingency = np.array(cont_list)

    alpha = float(input(f'Введите уровень значимости альфа: '))

    # Вычислим сумму по столбцам матрицы
    col = contingency.shape[1]
    sum_col_list = []
    for j in range(col):
        sum_col = sum(contingency[:, j])
        sum_col_list.append(sum_col)

    # Собираем всю матрицу, добавляя нижнюю строку с суммами значений столбцов
    contingency = np.vstack([contingency, sum_col_list])
    print('Матрица сопряжённости\n', contingency)

    # Вычислим статистику хи-квадрат
    khi_2 = 0
    k, m = contingency.shape
    # print(k, m)
    for i in range(k - 1):
        for j in range(m - 1):
            p = contingency[i][-1] * contingency[-1][j] / contingency[-1][-1]
            khi_2 += (contingency[i][j] - p) ** 2 / p
    print(f'Хи-квадрат {khi_2:.3f}')

    # P-значение для статистики критерия хи-квадрат
    degree_free = (m - 2) * (k - 2)  # так как k, m получаем из contingency, то нужно отнимать 2, а не 1
    edge_khi_2 = scipy.stats.chi2.ppf(1 - alpha, df=degree_free)
    print(f'Р-значение для критерия хи-квадрат {edge_khi_2:.3f}')
    if khi_2 > edge_khi_2:
        print('Гипотеза H0 отвергается в пользу альтернативной, так как статистика критерия попала в К.О.')
    else:
        print('Гипотеза H0 принимается')

    # Вычислим нормированные коэффициенты связи

    # Коэффициент Пирсона
    P = np.sqrt(khi_2 / (contingency[-1][-1] + khi_2))
    print(f'Коэффициент Пирсона {P:.3f}')

    # Коэффициент Чупрова
    T = np.sqrt(khi_2 / (contingency[-1][-1] * np.sqrt(degree_free)))
    print(f'Коэффициент Чупрова {T:.3f}')

    # Коэффициент Крамера
    list_degree = [k - 1, m - 1]
    min_set_degree = set(list_degree)
    K = np.sqrt(khi_2 / (contingency[-1][-1] * min(min_set_degree)))
    print(f'Коэффициент Крамера {K:.3f}')

    if m - 1 == k - 1 == 2:
        # Коэффициент среднеквадратической сопряжённости
        phi = np.sqrt(khi_2 / contingency[-1][-1])
        print(f'Коэффициент среднеквадратической сопряжённости {phi:.3f}')

        # Коэффициент контингенции
        fi = ((contingency[0][0] * contingency[1][1]) - (contingency[0][1] * contingency[1][0])) / \
             np.sqrt((contingency[0][0] + contingency[0][1]) * (contingency[1][0] + contingency[1][1]) * \
                     (contingency[0][0] + contingency[1][0] * (contingency[0][1] + contingency[1][1])))
        print(f'Коэффициент контингенции {fi:.3f}')

        # Коэффициент ассоциации
        Q = ((contingency[0][0] * contingency[1][1]) - (contingency[0][1] * contingency[1][0])) / \
            ((contingency[0][0] * contingency[1][1]) + (contingency[0][1] * contingency[1][0]))
        print(f'Коэффициент ассоциации {Q:.3f}')

    # Мера прогноза Гутмана
    sort_row = sorted(contingency[k - 1])  # Сортируем последнюю строку
    pb1 = 1 - sort_row[-2] / contingency[-1][-1]
    max_score_row = 0
    for i in range(k - 1):  # Находим максимум в каждой строке и делим на n
        sort = sorted(contingency[i])
        max_score_row += sort[-2] / contingency[-1][-1]
    pb2 = 1 - max_score_row
    lambda_b = (pb1 - pb2) / pb1
    print(f'Мера прогноза Гутмана (лямбда b) {lambda_b:.3f}')

    sort_col = sorted(contingency[:, m - 1])  # Сортируем последний столбец
    pa1 = 1 - sort_col[-2] / contingency[-1][-1]
    max_score_col = 0
    for i in range(m - 1):  # Находим максимум в каждом столбце и делим на n
        sort = sorted(contingency[:, i])
        max_score_col += sort[-2] / contingency[-1][-1]
    pa2 = 1 - max_score_col
    lambda_a = (pa1 - pa2) / pa1
    print(f'Мера прогноза Гутмана (лямбда a) {lambda_a:.3f}')
    print('Вычисления окончены!')


# Задача 1.1
# По данным исследования «Мониторинг социальных и экономических перемен в России» составлена следующая таблица
# сопряженности.
# Вопрос А: «Как бы Вы оценили в настоящее время материальное положение вашей семьи?» (Хорошее, среднее, плохое).
# Вопрос В: «Как бы Вы оценили в целом политическую обстановку в России?» (Благополучная, напряжённая,
# взрывоопасная критическая)
# A     B   Благоприятная Напряженная Взрывоопасная критическая
# Хорошее       12              48              47
# Среднее       20              478             666
# Плохое        11              160             701
dependency_research()

# Задача 1.2
# Изучается зависимость выбираемой абитуриентами специальности от пола. Было опрошено 480 человек и получены следующие
# результаты:
#
# Специальность     Пол  M    Ж
# Естественные науки    168   92
# Гуманитарные науки    85    135
#
# Можно ли на уровне доверия 0,95 считать, что между полом и выбором специальности есть связь?
# Оцените силу связи с помощью различных коэффициентов.
dependency_research()
