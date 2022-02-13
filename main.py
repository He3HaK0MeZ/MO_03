import SimplexMethod.simplextable as sim_table
import source as src


if __name__ == '__main__':
    filename = 'data.txt'
    data = [line.replace('\n', '') for line in open(filename)]

    table = sim_table.SimplexTable(data)

    answer = src.solve_clp(data, table)
    src.print_answer_clp(data, answer)
