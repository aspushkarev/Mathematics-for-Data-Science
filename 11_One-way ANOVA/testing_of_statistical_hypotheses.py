import math
import scipy.stats as stats

import numpy as np
from scipy.stats import norm


def testing_of_statistical_hypotheses(first_positive, first_total, second_positive, second_total, param):
    '''
    By default p1 > p2. Critical region is right.
    :param first_positive: Success on first series
    :param first_total: Total first series
    :param second_positive: Success second series
    :param second_total: Total second series
    :param alpha: Significance level
    :return:    Test statistic
                The answer to the question accepts or rejects the main hypothesis at the selected level significance
                P-value
    '''
    first_list = []
    second_list = []
    total_list = []

    first_list.append(first_positive)
    first_negative = first_total - first_positive
    first_list.append(first_negative)
    first_list.append(first_total)

    second_list.append(second_positive)
    second_negative = second_total - second_positive
    second_list.append(second_negative)
    second_list.append(second_total)

    total_list.append(first_positive + second_positive)
    total_list.append(first_negative + second_negative)
    total_list.append(total_list[0] + total_list[1])

    # Вычисляем статистику критерия
    prob_positive = total_list[0] / total_list[2]
    test_statistic = ((first_list[0] / first_list[2]) - (second_list[0] / second_list[2])) / \
                     math.sqrt(prob_positive * (1 - prob_positive) * ((1 / first_list[2]) + (1 / second_list[2])))
    print(f'Test statistic is {test_statistic:0.2f}')

    # Принимаем решение
    if test_statistic < param:
        print('We are accept the main hypothesis at the selected level significance')
    else:
        print('We are reject the main hypothesis at the selected level significance')

    # Стандартизированное нормальное распределение
    norm_rv = stats.norm(loc=0, scale=1)
    z_score = norm_rv.cdf(test_statistic)
    print(f'Z-score is {z_score:0.2f}')

    # Вычисляем P-value
    probability = 1 - z_score
    print(f'P-value is {probability:0.2f}')


def mann_whitney_wilcoxon_test(alternative):
    '''
    :param alternative: {‘two-sided’, ‘less’, ‘greater’}
    :return: w, mean, variance, statistic, p-value
    '''

    # First sample X
    x = list(map(float, input('Enter the elements of the first sample separated by a space:').split()))
    # task three
    # x = [130, 110, 120, 140, 200, 130, 140, 170, 160, 140]
    # task four
    # x = [102.4, 100.0, 67.6, 65.9, 64.7, 39.6, 31.2]
    # example from lesson
    # x = [30, 28, 46, 42, 35, 33, 44, 43, 31, 38]

    # Second sample Y
    y = list(map(float, input('Enter the elements of the second sample separated by a space:').split()))
    # task three
    # y = [120, 190, 130, 160, 150, 120, 110, 120, 200]
    # task four
    # y = [48.1, 45.5, 41.7, 35.4, 29.1, 18.9, 58.3, 68.8, 71.3, 94.3]
    # example from lesson
    # y = [26, 37, 39, 28, 31, 27, 32, 35]

    sorted_x = sorted(x)
    sorted_y = sorted(y)
    # print(f'sorted_x', sorted_x)
    # print(f'sorted_y', sorted_y)
    sorted_x_copy = sorted_x.copy()
    sorted_y_copy = sorted_y.copy()
    current_x = sorted_x_copy[0]
    current_y = sorted_y_copy[0]
    length = len(set(sorted_x_copy + sorted_y_copy))
    rank = 1
    rank_x = []
    rank_y = []
    while length != 0:
        # print('length =', length)
        count_similar_x = 0
        count_similar_y = 0

        for i in sorted_x_copy:
            if i == current_x:
                count_similar_x += 1
                # print(f'count_similar_x', count_similar_x)
            elif i > current_x:
                break

        for j in sorted_y_copy:
            if j == current_y:
                count_similar_y += 1
                # print(f'count_similar_y', count_similar_y)
            elif j > current_y:
                break

        if current_x == current_y:
            # print('current_x==current_y')
            # print('current_x', current_x)
            # print('current_y', current_y)
            rank_old = rank
            count_similar = count_similar_x + count_similar_y
            rank = rank + (1 / count_similar)
            for _ in range(count_similar_x):
                rank_x.append(round(rank, 2))
            for _ in range(count_similar_y):
                rank_y.append(round(rank, 2))

            rank = rank_old + count_similar
            # print('rank ', rank)

            while count_similar_x != 0:
                # print('Delete x', current_x)
                sorted_x_copy.remove(current_x)
                count_similar_x -= 1

            while count_similar_y != 0:
                # print('Delete y', current_y)
                sorted_y_copy.remove(current_y)
                count_similar_y -= 1

        elif current_x > current_y:
            rank_old = rank

            if count_similar_y > 1:
                rank_old = rank
                rank = rank + (1 / count_similar_y)
                for _ in range(count_similar_y):
                    rank_y.append(round(rank, 2))
            else:
                rank_y.append(rank)

            rank = rank_old + count_similar_y

            while count_similar_y != 0:
                # print('Delete y', current_y)
                sorted_y_copy.remove(current_y)
                count_similar_y -= 1

        elif current_x < current_y:
            rank_old = rank

            if count_similar_x > 1:
                rank = rank + (1 / count_similar_x)
                for _ in range(count_similar_x):
                    rank_x.append(round(rank, 2))
            else:
                rank_x.append(rank)

            rank = rank_old + count_similar_x
            # print('rank', rank)
            while count_similar_x != 0:
                # print('Delete x', current_x)
                sorted_x_copy.remove(current_x)
                count_similar_x -= 1

        if len(sorted_x_copy) == 0:
            current_x = 99999
        else:
            current_x = sorted_x_copy[0]

        if len(sorted_y_copy) == 0:
            current_y = 99999
        else:
            current_y = sorted_y_copy[0]

        # print(f'sorted_x_copy', sorted_x_copy)
        # print(f'sorted_y_copy', sorted_y_copy)
        # print('current_x', current_x)
        # print('current_y', current_y)
        # print('rank_x', rank_x)
        # print('rank_y', rank_y)
        length -= 1

    w = sum(rank_y)
    print(f'W = {w:0.2f}')

    mean = (len(y) / 2) * (len(x) + len(y) + 1)
    print('Mean =', mean)
    variance = (len(x) * len(y)) / 12 * (len(x) + len(y) + 1)
    print(f'Variance = {variance:0.2f}')
    statistic = (w - mean) / np.sqrt(variance)
    print(f'Statistic = {statistic:0.2f}')

    # Доверительная и критическая области
    norm_rv = stats.norm(loc=0, scale=1)
    z_score = norm_rv.cdf(statistic)
    print(f'zscore = {z_score:0.2f}')

    if alternative == 'two-sided':
        # print('two-sided')
        param11 = -1.96
        param12 = 1.96
        minimum = min(2 * z_score, 2 - 2 * z_score)
        print(f'P-value = {minimum:0.2f}')

        # Принимаем решение
        if param11 < statistic < param12:
            print('We are accept the main hypothesis at the selected level significance')
        else:
            print('We are reject the main hypothesis at the selected level significance')

    elif alternative == 'greater':
        # print('greater')
        param2 = 1.6449
        print(f'P-value = {1 - z_score:0.2f}')

        # Принимаем решение
        if statistic < param2:
            print('We are accept the main hypothesis at the selected level significance')
        else:
            print('We are reject the main hypothesis at the selected level significance')

    elif alternative == 'less':
        # print('less')
        param3 = -1.6449
        print(f'P-value = {z_score:0.2f}')

        # Принимаем решение
        if statistic > param3:
            print('We are accept the main hypothesis at the selected level significance')
        else:
            print('We are reject the main hypothesis at the selected level significance')


# Перед президентскими выборами в городах Курске и Владивостоке был проведен
# социологический опрос. Каждый респондент должен был ответить на вопрос:
# «За какого кандидата вы будете голосовать на выборах». В Курске опросили
# 105 человек, из них 42 ответили, что будут голосовать за кандидата А, во
# Владивостоке опросили 195 человек, из которых 65 за А. Можно ли считать
# на уровне значимости 0,05, что уровни поддержки кандидата А в Курске и
# Владивостоке одинаковы?
print('The first task')
testing_of_statistical_hypotheses(42, 105, 65, 195, 1.645)

# Для изучения эффективности лекарства против аллергии обследовались две
# группы людей, предрасположенных к этому заболеванию. Результаты обследования
# следующие: среди принимавших лекарство заболело 3 человека, не заболело
# 172 человека; среди не принимавших заболело 32 человека, не заболело 168.
# Указывают ли эти результаты на эффективность лекарства?
print('\nThe second task')
testing_of_statistical_hypotheses(172, 175, 168, 200, 1.645)

# Было проведено обследование 10 горожан и 9 жителей села примерно одного
# возраста. Получены следующие данные об уровне давления:
# для горожан: 130, 110, 120, 140, 200, 130, 140, 170, 160, 140;
# для селян: 120, 190, 130, 160, 150, 120, 110, 120, 200.
# Свидетельствуют ли эти данные в пользу того, что горожане имеют в среднем
# более высокое давление чем жители сельской местности?
print('\nThe third task')
mann_whitney_wilcoxon_test(alternative='greater')
# x = [130, 110, 120, 140, 200, 130, 140, 170, 160, 140]
# y = [120, 190, 130, 160, 150, 120, 110, 120, 200]

# Уровень гистамина в мокроте у 7 курильщиков, склонных к аллергии,
# составил в мг: 102,4 100,0 67,6 65,9 64,7 39,6 31,2
# У 10 курильщиков, не склонных к аллергии, составил в мг:
# 48,1 45,5 41,7 35,4 29,1 18,9 58,3 68,8 71,3 94,3
# Можно ли, основываясь на этих данных, считать с надёжностью 0,95 что уровень
# гистамина у склонных и не склонных к аллергии курильщиков значимо различается?
print('\nThe fourth task')
mann_whitney_wilcoxon_test(alternative='two-sided')
# x = [102.4, 100.0, 67.6, 65.9, 64.7, 39.6, 31.2]
# y = [48.1, 45.5, 41.7, 35.4, 29.1, 18.9, 58.3, 68.8, 71.3, 94.3]
