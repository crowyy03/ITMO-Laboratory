class Matrix:
    def __init__(self, height, width, matrix=None, CSR_matrix=None):
        self.width = width
        self.height = height
        if CSR_matrix is None:
            self.values = []
            self.col_index = []
            self.li = [0]
            for i in matrix:
                for j, value in enumerate(i):
                    if value != 0:
                        self.values.append(value)
                        self.col_index.append(j)
                self.li.append(len(self.values))
        else:
            self.values = CSR_matrix[0]
            self.col_index = CSR_matrix[1]
            self.li = CSR_matrix[2]
        # print(self.values)
        # print(self.col_index)
        # print(self.li)

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
        values = []
        col_index = []
        li = [0]
        indrow = 0
        for i in range(self.height):
            sta, fna = self.li[i], self.li[i + 1]
            stb, fnb = other.li[i], other.li[i + 1]
            inda, indb = sta, stb
            while inda < fna or indb < fnb:
                if inda == fna:
                    values.append(other.values[indb])
                    col_index.append(other.col_index[indb])
                    indb += 1
                    indrow += 1
                elif indb == fnb:
                    values.append(self.values[inda])
                    col_index.append(self.col_index[inda])
                    inda += 1
                    indrow += 1
                elif self.col_index[inda] == other.col_index[indb]:
                    values.append(self.values[inda] + other.values[indb])
                    col_index.append(self.col_index[inda])
                    inda += 1
                    indb += 1
                    indrow += 1
                elif self.col_index[inda] < other.col_index[indb]:
                    values.append(self.values[inda])
                    col_index.append(self.col_index[inda])
                    inda += 1
                    indrow += 1
                else:
                    values.append(other.values[indb])
                    col_index.append(other.col_index[indb])
                    indb += 1
                    indrow += 1
            li.append(indrow)
        return Matrix(self.height, self.width, CSR_matrix=[values, col_index, li])

    def __mul__(self, other):
        if type(other) is Matrix:
            if self.width != other.height:
                raise MatrixError("Ошибка в размерностях матриц")
            values = []
            col_index = []
            li = [0]
            row_pt = 0
            for row_a in range(self.height):
                row_c_values = []
                row_c_col_index = []
                start_a = self.li[row_a]
                end_a = self.li[row_a + 1]
                for idx_a in range(start_a, end_a):
                    col_a = self.col_index[idx_a]
                    value_a = self.values[idx_a]
                    start_b = other.li[col_a]
                    end_b = other.li[col_a + 1]
                    for idx_b in range(start_b, end_b):
                        col_b = other.col_index[idx_b]
                        value_b = other.values[idx_b]
                        product = value_a * value_b
                        if col_b in row_c_col_index:
                            index = row_c_col_index.index(col_b)
                            row_c_values[index] += product
                        else:
                            row_c_col_index.append(col_b)
                            row_c_values.append(product)
                sorted_index = sorted(row_c_col_index)
                for i in range(len(sorted_index)):
                    col_index.append(row_c_col_index[i])
                    values.append(row_c_values[i])
                    row_pt += 1
                li.append(row_pt)
            return Matrix(self.height, other.width, CSR_matrix=[values, col_index, li])
        elif type(other) is int:
            values = [i * other for i in self.values]
            return Matrix(self.height, self.width, CSR_matrix=[values, self.col_index, self.li])
        else:
            raise MatrixError(f"Вы не можете умножить матрицу на {type(other)}")

    def __rmul__(self, other):
        if type(other) is int:
            values = [i * other for i in self.values]
            return Matrix(self.height, self.width, CSR_matrix=[values, self.col_index, self.li])
        else:
            raise MatrixError(f"Вы не можете умножить матрицу на {type(other)}")

    def get_element(self, row, col):
        if 0 >= row > self.height or 0 >= col > self.width:
            raise MatrixError("Индексы за пределами матрицы")
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
            determinant += ((-1) ** i) * matrix[0][i] * Matrix(len(minor), len(minor[0]), minor).get_determinant()
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


def main():
    # n, m = map(int, input().split())
    # matrix = Matrix(n, m, [list(map(int, input().split())) for _ in range(n)])
    #
    # n1, m1 = map(int, input().split())
    # matrix1 = Matrix(n1, m1, [list(map(int, input().split())) for _ in range(n1)])
    #
    # print(matrix * matrix1)
    # matrix0 = Matrix(5, 5, [[1, 1, 345, 1, 4], [2, 0, 0, 23, 5], [124, 0, 345, 4, 0], [0, 124, 0, 13, 1],
    #                         [13, 1213, 32, 3, 1]])
    a = Matrix(3, 5, [[0, 3, 4, 7, 8], [0, 0, 1, 7, 6], [7, 8, 0, 6, 4]])
    # print('=============')
    b = Matrix(5, 3, [[3, 0, 4], [8, 0, 2], [0, 7, 5], [4, 3, 1], [123, 4, 1]])
    # print(a)
    # print(b)
    # print('=============')
    c = a * b
    # print(a)
    # print(b)
    print(c)
    # matrix1 = Matrix(5, 5,
    #                  [[1, 1, 1, 1, 4], [2, 0, 0, 23, 5], [124, 0, 12, 4, 0], [0, 0, 0, 13, 1], [13, 123, 32, 3, 1]])
    # print(matrix0)
    # print(matrix0.get_trace())


if __name__ == '__main__':
    main()
