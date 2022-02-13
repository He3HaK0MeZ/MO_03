import SimplexMethod.logic as fl


class SimplexTable:
    def __init__(self, data):
        # количество строк таблицы
        self.__rows = row_count(data) + 1
        # количество столбцов таблицы
        self.__cols = column_count(data) + 1
        # таблица
        self.__table = create_table(data)
        # номер разрешающей строки
        self.__permRow = -1
        # номер разрешающего столбца
        self.__permCol = -1
        # разрешающий элемент
        self.__permEl = 0.0

    # функция вывода симплекс-таблицы
    def print_table(self):
        for line in self.__table:
            for el in line:
                print(str(el).ljust(25), end='')
            print('\n\n')

    # функция нахождения опорного решения
    def find_pivot(self):
        permissive_col = -1
        # анализируем столбец свободных членов
        for i in range(1, self.__rows - 1):
            # находим первое отрицательное число
            if float(self.__table[i][1]) < 0:
                # анализируем строку с найденным отрицательным свободным членом
                for j in range(2, self.__cols):
                    # ищем первое отрицательное число в найденной строке
                    if float(self.__table[i][j]) < 0:
                        # индекс разрешающего столбца:
                        permissive_col = j
                        break
                # если в строке нет отрицательных, то допустимых решений нет
                if permissive_col == -1:
                    print("Допустимых решений нет", end='\n\n')
                    return False
                else:
                    break
        if permissive_col != -1:
            permissive_row = -1
            min_attitude = 1000000
            # анализируем столбцы для нахождения минимального модуля отношения столбца свободных членов к разрешающему
            for i in range(1, self.__rows - 1):
                if float(self.__table[i][permissive_col]) != 0.0 and float(self.__table[i][1]) != 0.0:
                    attitude = float(self.__table[i][1]) / float(self.__table[i][permissive_col])
                    if 0.0 <= attitude < min_attitude:
                        min_attitude = attitude
                        permissive_row = i
            # индекс разрешающей строки:
            self.__permRow = permissive_row
            self.__permCol = permissive_col
            # разрешающий элемент
            self.__permEl = self.__table[self.__permRow][self.__permCol]
            return True
        return False

    # функция нахождения оптимального решения
    def find_optimal(self):
        # вектор положительных элементов целевой функции без свободного члена
        permissive_col = -1
        for i in range(2, self.__cols):
            if float(self.__table[self.__rows - 1][i]) > 0:
                permissive_col = i
                break
        if permissive_col != -1:  # если в строке F есть положительный элемент
            permissive_row = -1
            min_attitude = 1000000
            for i in range(1, self.__rows - 1):
                # если в столбце есть положительные элементы, то он разрешающий
                if float(self.__table[i][permissive_col]) > 0 and \
                        abs(float(self.__table[i][1]) / float(self.__table[i][permissive_col])) < min_attitude:
                    min_attitude = abs(float(self.__table[i][1]) / float(self.__table[i][permissive_col]))
                    permissive_row = i
            # если в столбце нет положительных элементов, то оптимального решения не существует
            if permissive_row == -1:
                print("Функция не ограничена снизу, оптимального решения не существует")
                return False
            # информация о разрешающем элементе
            self.__permRow = permissive_row
            self.__permCol = permissive_col
            self.__permEl = self.__table[permissive_row][permissive_col]
            return True
        else:  # если в строке F нет положительных элементов, то решение оптимально
            print('Решенная симплекс-таблица:', end='\n\n')
            self.print_table()
            print('Найденное решение оптимально', end='\n\n')
            return False

    # функкция печати информации о разрешающем элементе таблицы
    def print_access_el(self):
        print('Индекс разрешающей строки - ', self.__permRow)
        print('Индекс разрешающего столбца - ', self.__permCol)
        print('Разрешающий элемент - ', self.__table[self.__permRow][self.__permCol], end='\n\n')

    # Жорданово исключение
    def jordan_exception(self):
        # перемена мест заголовков разрешающей строки и столбца
        self.__table[0][self.__permCol], self.__table[self.__permRow][0] = \
            self.__table[self.__permRow][0], self.__table[0][self.__permCol]
        # сохранение первоначального разрешающего элемента
        pivot = float(self.__permEl)
        # обновление всех членов вне разрещающей строки и столбца
        for i in range(1, self.__rows):
            for j in range(1, self.__cols):
                if i != self.__permRow and j != self.__permCol:
                    self.__table[i][j] = str(float(self.__table[i][j]) - float(self.__table[self.__permRow][j]) *
                                             float(self.__table[i][self.__permCol]) / pivot)
        # обновление членов внутри разрешающей строки и столбца
        for i in range(1, self.__rows):
            for j in range(1, self.__cols):
                if i == self.__permRow:
                    if j == self.__permCol:
                        self.__permEl = 1 / pivot
                        self.__table[i][j] = str(self.__permEl)
                    else:
                        self.__table[i][j] = str(float(self.__table[i][j]) / pivot)
                else:
                    if j == self.__permCol:
                        self.__table[i][j] = str(- float(self.__table[i][j]) / pivot)

    # функция выполнения сиплекс-метода
    def find_solution(self):
        print('Начальная симплекс-таблица:', end='\n\n')
        self.print_table()
        vec = []
        # находим опорное решение, пока все элементы в столбце свободных членов не станут положительными
        while True:
            for i in range(1, self.__rows - 1):
                if float(self.__table[i][1]) < 0:
                    vec.append(self.__table[i][1])
            # если в столбце свободных членов есть отрицательные, то находим опорное решение
            if vec:
                if self.find_pivot():
                    self.jordan_exception()
                    vec.clear()
                else:
                    return False
            else:
                break
        while self.find_optimal():
            self.jordan_exception()
        return True

    # функция печати ответа
    def print_answer(self, data):
        print('Ответ:')
        for i in range(2, self.__cols):
            print(self.__table[0][i], '=', end=' ')
        print('0.0')
        for i in range(1, self.__rows - 1):
            print(self.__table[i][0], '=', self.__table[i][1])
        if '->max' in data[-1]:
            print(self.__table[-1][0], '=', -float(self.__table[-1][1]), '(для F -> max)', end='\n\n')
        else:
            print(self.__table[-1][0], '=', self.__table[-1][1], '(для F -> min)', end='\n\n')

    # функция получения пар значений начальная переменная - оптимальное значение
    def get_base_dict(self):
        var_dict = {}
        count = self.__cols - 2
        for i in range(2, self.__cols):
            if self.__table[0][i] < 'x' + str(count + 1):
                var_dict[self.__table[0][i]] = 0.0
        for i in range(1, self.__rows - 1):
            if self.__table[i][0] < 'x' + str(count + 1):
                var_dict[self.__table[i][0]] = float(self.__table[i][1])
        return var_dict

    # функция нахождения значения целевой функции
    def get_target(self, data):
        if '->max' in data[-1]:
            return -float(self.__table[-1][1])
        return float(self.__table[-1][1])


# функция нахождения количества столбцов матрицы
def column_count(data):
    return fl.var_count(data) + 1


# функция нахождения количества строк матрицы
def row_count(data):
    return len(data)


# функция создания верхней строки
def headline(data):
    vec = ['', 'S']
    count = fl.var_count(data)
    for i in range(1, count + 1):
        vec.append('x' + str(i))
    return vec


# функция создания левого столбца
def headcolumn(data):
    vec = []
    for i in range(fl.var_count(data) + 1, fl.var_count(data) + fl.fictitious_var_count(data) + 1):
        vec.append('x' + str(i))
    vec.append('F')
    return vec


# функция создания матрицы симплекс-таблицы
def create_matrix(data):
    free = fl.free_vec(data)
    mat = fl.parse(data)
    cols = column_count(data)
    rows = row_count(data)
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(1, cols):
            matrix[i][0] = free[i]
            matrix[i][j] = mat[i][j - 1]
            if '->max' in data[-1] and i == rows - 1:
                matrix[i][j] *= -1
    return matrix


# функция создания симплекс-таблицы
def create_table(data):
    head_l = headline(data)
    head_col = headcolumn(data)
    rows = row_count(data)
    cols = column_count(data)
    matrix = create_matrix(data)
    table = [head_l]
    for i in range(1, rows + 1):
        vec = [head_col[i - 1]]
        for j in range(1, cols + 1):
            vec.append(matrix[i - 1][j - 1])
        table.append(vec)
    return table
