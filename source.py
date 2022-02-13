import SimplexMethod.simplextable as sim_table
import math


# функция сортировки словаря по ключу
def dict_sort(unsorted_dict):
    sorted_keys = sorted(unsorted_dict.keys())
    sorted_dict = {}
    for i in sorted_keys:
        sorted_dict[i] = unsorted_dict[i]
    return sorted_dict


# функция нахождения переменной ветвления
def find_branch_var(solution_dict):
    # создаём словарь отсортированный по ключам
    sorted_dict = dict_sort(solution_dict)
    branch_var = ''
    for i in sorted_dict.keys():
        # если найдется дробное число, то его ключ становится переменной ветвления
        if math.modf(sorted_dict[i])[0] != 0.0:
            branch_var = i
            break
    return branch_var


# проверка наличия переменной ветвления
def is_int(branch_var):
    if not branch_var:
        print('Решение целочисленное', end='\n\n')
        return True
    else:
        print(branch_var, '- переменная ветвления', end='\n\n')
        return False


# функция получения целых чисел для ветвления
def find_limits(solution_dict, branch_var):
    lower_limit = int(math.modf(solution_dict[branch_var])[1])
    upper_limit = lower_limit + 1
    return [lower_limit, upper_limit]


def solve_clp(data, table):
    if table.find_solution():
        table.print_answer(data)
        # находим словарь со значениями начальных переменных
        solution_dict = table.get_base_dict()
        print(solution_dict)
        # находим переменную ветвления
        branch_var = find_branch_var(solution_dict)
        # если переменная целочисленная, то завершаем процесс
        if is_int(branch_var):
            solution_dict['F'] = table.get_target(data)
            return solution_dict
        # находим список из нижнего и верхнего ограничения для переменной ветвления
        limit_vec = find_limits(solution_dict, branch_var)
        solution_vec = []
        # вводим ограничения xi <= limit_vec[0]
        for i in range(2):
            new_data = list(data)  # создание новой системы
            if i == 0:
                new_limit = branch_var + '<=' + str(limit_vec[0])
                print('Левая ветвь дерева:', new_limit, end='\n\n')
                new_data.insert(-1, new_limit)
            else:
                new_limit = branch_var + '>=' + str(limit_vec[1])
                print('Правая ветвь дерева:', new_limit, end='\n\n')
                new_data.insert(-1, new_limit)
            new_table = sim_table.SimplexTable(new_data)
            answer = solve_clp(new_data, new_table)
            if type(answer) == dict:
                solution_vec.append(answer)
            elif type(answer) == list:
                solution_vec.extend(answer)
            new_data.clear()
        return solution_vec
    return False


# функция печати
def print_answer_clp(data, solution_vec):
    print('Ответ:')
    if '->max' in data[-1]:
        max_target = -1
        answer = {}
        for solution_dict in solution_vec:
            if solution_dict['F'] > max_target:
                max_target = solution_dict['F']
                answer = solution_dict
    else:
        min_target = 1000000
        answer = {}
        for solution_dict in solution_vec:
            if solution_dict['F'] < min_target:
                min_target = solution_dict['F']
                answer = solution_dict
    for key in answer.keys():
        print(key, '=', answer[key])
