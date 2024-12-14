class Matrix:
    def __init__(self, height, width, matrix):
        self.width = width
        self.height = height
        self.values = []
        self.col_index = []
        self.li = [0]
        for i in matrix:
            for j, value in enumerate(i):
                if value != 0:
                    self.values.append(value)
                    self.col_index.append(j)
            self.li.append(len(self.values))

    def __str__(self):
        matrix = [[self.get_element(i + 1, j + 1) for j in range(self.width)] for i in range(self.height)]
        max_width = max(len(str(elem)) for row in matrix for elem in row)
        formatted_rows = [" ".join(f"{elem:^{max_width}}" for elem in row) for row in matrix]
        formatted_matrix = []
        for i, row in enumerate(formatted_rows):
            if i == 0:
                formatted_matrix.append(f"▞ {row} ▚")
            elif i == len(formatted_rows) - 1:
                formatted_matrix.append(f"▚ {row} ▞")
            else:
                formatted_matrix.append(f"| {row} |")
        return "\n".join(formatted_matrix)

    def __add__(self, other):
        if self.width != other.width or self.height != other.height:
            raise MatrixError("Размерности должны совпадать")
        new_matrix = []
        for i in range(self.height):
            new_matrix.append(
                [self.get_element(i + 1, j + 1) + other.get_element(i + 1, j + 1) for j in range(self.width)])
        return Matrix(self.height, self.width, new_matrix)

    def __mul__(self, other):
        if type(other) is Matrix:
            if self.width != other.height:
                raise MatrixError("Ошибка в размерностях матриц")
            new_matrix = [[(sum([self.get_element(i + 1, k + 1) * other.get_element(k + 1, j + 1) 
                for k in range(self.width)])) 
                for j in range(other.width)] 
                for i in range(self.height)]
            return Matrix(self.height, other.width, new_matrix)
        elif type(other) is int:
            new_matrix = [[self.get_element(i + 1, j + 1) * other 
                           for j in range(self.width)] 
                           for i in range(self.height)]
            return Matrix(self.height, self.width, new_matrix)
        else:
            raise MatrixError(f"Вы не можете умножить матрицу на {type(other)}")

    def get_element(self, row, col):
        try:
            return self.values[self.col_index[self.li[row - 1]:self.li[row]].index(col - 1) + self.li[row - 1]]
        except:
            return 0

    def get_trace(self):
        if self.width != self.height:
            raise MatrixError("Невозможно посчитать след для неквадратной матрицы")
        return sum([self.get_element(i + 1, i + 1) for i in range(self.height)])

    def get_determinant(self):
        if self.width != self.height:
            raise MatrixError("Невозможно посчитать определитель для неквадратной матрицы")
        matrix = [[self.get_element(i + 1, j + 1) for j in range(self.width)] for i in range(self.height)]
        if self.width == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        determinant = 0
        for i in range(self.width):
            minor = [j[:i] + j[i + 1:] for j in matrix[1:]]
            determinant += ((-1) ** i) * matrix[0][i] * Matrix(len(minor), 
                                        len(minor[0]), minor).get_determinant()
        return determinant

    def exist_inverse_matrix(self):
        if self.get_determinant() != 0:
            print("Да")
            return True
        else:
            print("Нет")
            return False


class MatrixError(Exception):
    def __init__(self, message):
        super().__init__(message)


# n, m = map(int, input().split())
#
# matrix = Matrix(n, m, [list(map(int, input().split())) for _ in range(n)])
matrix0 = Matrix(5, 5, [[1, 1, 345, 1, 4], [2, 0, 0, 23, 5], [124, 0, 345, 4, 0], [0, 124, 0, 13, 1], [13, 1213, 32, 3, 1]])
matrix1 = Matrix(5, 5, [[1, 1, 1, 1, 4], [2, 0, 0, 23, 5], [124, 0, 12, 4, 0], [0, 0, 0, 13, 1], [13, 123, 32, 3, 1]])
matrix2 = Matrix(2, 2, [[1, 1], [2, 2]])
matrix3 = Matrix(2, 3, [[1, 1, 1], [2, 2, 2]])
matrix4 = matrix2 * matrix3
matrix5 = matrix0 + matrix1
print(matrix5)
print(matrix4)
# print(matrix1.get_determinant())
