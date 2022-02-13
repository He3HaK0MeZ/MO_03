# функция нахождения последнего 'x'
def find_last(string):
    last_x = 0
    index = 0
    for ch in string:
        if ch == 'x':
            last_x = index
        index += 1
    return last_x


# функция нахождения количества переменных
def var_count(data):
    vec = []
    for string in data:
        if 'F=' in string:
            if '->max' in string:
                string = string.replace('->max', '')
            else:
                string = string.replace('->min', '')
        vec.append(int(string[find_last(string) + 1]))
    return max(vec)


# функция нахождения количества фиктивных переменных
def fictitious_var_count(data):
    return len(data) - 1


# функция нахождения свободных членов
def free_vec(data):
    vec = []
    for string in data:
        if 'F=' not in string:
            if '<=' in string:
                vec.append(float(string[(string.find('=') + 1):]))
            else:
                vec.append(-float(string[(string.find('=') + 1):]))
        else:
            vec.append(0.0)
    return vec


# функция составления матрицы из коэффициентов при переменных и из целевой функции
def parse(data):
    matrix = []
    for string in data:
        vec = []
        if 'F=' in string:
            string = string.replace('F=', '')
            if '->max' in string:
                string = string.replace('->max', '')
            else:
                string = string.replace('->min', '')
        iterator = 0
        for i in range(1, var_count(data) + 1):
            var = 'x' + str(i)
            if var not in string:
                vec.append('0')
                continue
            if '<=' in string:
                vec.append(string[iterator:string.find(var)])
                iterator += 1
            else:
                vec.append('-' + string[iterator:string.find(var)])
            iterator += len(vec[-1]) + len(str(i))
        for i in range(len(vec)):
            if '--' in vec[i]:
                vec[i] = vec[i].replace('--', '+')
            if '-+' in vec[i]:
                vec[i] = vec[i].replace('-+', '-')
            if vec[i] == '' or vec[i] == '+':
                vec[i] = 1.0
            elif vec[i] == '-':
                vec[i] = -1.0
            else:
                vec[i] = float(vec[i])
        matrix.append(vec)
    return matrix
