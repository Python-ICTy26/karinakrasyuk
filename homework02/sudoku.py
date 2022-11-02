import pathlib
import time
import typing as tp
from random import randint

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[str], n: int) -> tp.List[tp.List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    matrix: tp.List[tp.List[str]]
    matrix = [[] * n for i in range(n)]  # создание пустого двумерного массива размера n * n

    for i in range(len(values)):  # пробегаем по элементам списка
        matrix[i // n] += [values[i]]  # добавление элемента в нужную строку
    return matrix


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """

    (row, col) = pos  # вытянул из пары отдельно строку и столбец
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    (row, col) = pos
    lst = []
    for j in range(len(grid)):
        lst += [grid[j][col]]

    return lst


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """

    (row, col) = pos
    row_block = (row // 3) * 3  # строка, с которой начинается блок
    col_block = (col // 3) * 3  # столбец, с которого начинается блок

    lst = []
    for i in range(row_block, row_block + 3):
        for j in range(col_block, col_block + 3):
            lst += [grid[i][j]]

    return lst


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """

    for i in range(len(grid)):  # количество строк
        for j in range(len(grid[i])):  # количество элементов в строке i
            if grid[i][j] == ".":  # если элемент матрицы равен точке
                return i, j

    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    values = set(str(i) for i in range(1, 10))
    row = set(get_row(grid, pos))
    col = set(get_col(grid, pos))
    block = set(get_block(grid, pos))

    return values - row - col - block


def solve(grid: tp.List[tp.List[str]]):
    """Решение пазла, заданного в grid"""
    """ 
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """

    """""
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    else:
        values = find_possible_values(grid, pos)
        (row, col) = pos
        for val in values:
            grid[row][col] = val 
            if solve(grid):
                return grid
            grid[row][col] = "." 
        return None
    """
    queue = [grid]

    while len(queue) > 0:
        cur_grid = queue.pop()

        pos = find_empty_positions(cur_grid)
        if not pos:
            return cur_grid
        else:
            (row, col) = pos
            values = find_possible_values(cur_grid, pos)
            for val in values:
                now_grid = list(list(x) for x in cur_grid)
                now_grid[row][col] = val
                queue.append(now_grid)

    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles
    all_values = set("123456789")
    for row in solution:  # прохожусь по всем строкам, где должны быть числа от 1 до 9
        if set(row) != all_values:  # если все элементы строки не равны от 1 до 9
            return False
    for col in range(9):  # прохожусь по каждому столбцу
        pos = (0, col)
        if set(get_col(solution, pos)) != all_values:
            return False
    for i in range(0, 9, 3):  # прохожусь по левому углу блока
        for j in range(0, 9, 3):
            pos = (i, j)
            block = get_block(solution, pos)
            if set(block) != all_values:
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """

    grid = [["."] * 9 for n in range(9)]
    grid = solve(grid)
    if N > 81:
        N = 81
    need = 81 - N  # точки туда поставить
    if need > 0:
        while need > 0:  # пока нужно расставлять точки
            row, col = randint(0, 8), randint(0, 8)
            if grid[row][col] != ".":  # если не равняется точке, то ставим точку
                grid[row][col] = "."
                need -= 1  # ставим точку на одну меньше
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        start = time.time()
        solution = solve(grid)
        end = time.time()

        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
            print(end - start)
