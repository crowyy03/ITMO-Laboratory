import numpy as np
import matplotlib.pyplot as plt
class Function:
    def __init__(self, func_str, a, b, epsilon, true_root=None):
        self.f = lambda x: eval(func_str)
        self.a, self.b, self.ep = a, b, epsilon
        self.true_root = true_root  
        self.extr_dih = []
        self.extr_gol = []

    def alg_dihotomia (self):
        a, b, ep = self.a, self.b, self.ep
        mid_point = []
        intervals = []
        while b - a > ep:
            intervals.append(float(b - a))
            left = (a + b - ep) / 2
            right = (a + b + ep) / 2
            if self.f(left) <= self.f(right):
                b = right
            else:
                a = left
            self.extr_dih.append((a + b) / 2)

            mid_point.append(float((a + b) / 2))


        self.graph(mid_point, intervals)
        return (a + b) / 2
        
    def alg_golden_ratio(self):
        a, b, ep = self.a, self.b, self.ep
        mid_point = []
        intervals = []
        phi = (1 + 5**0.5) / 2  
        inv_phi = 1 / phi
        while (b - a) > ep:
            intervals.append(float(b - a))
            left = b - (b - a) * inv_phi
            right = a + (b - a) * inv_phi
            if self.f(left) <= self.f(right):
                b = right
            else:
                a = left

            mid_point.append(float((a + b) / 2))

        self.graph(mid_point, intervals)
        return float((a + b) / 2)
        
    def root (self):
        a, b, ep = self.a, self.b, self.ep
        f = lambda x: self.f(x) - target
        
        # Проверка теоремы Больцано-Коши
        if self.f(a) * self.f(b) >= 0:
            raise FunctionError("На заданном интервале функция не меняет знак (нет корня).")

        while b - a >= ep:
            med = (a + b) / 2
            if abs(self.f(med)) < ep:
                return float(med)

            if self.f(a) * self.f(med) < 0:
                b = med
            elif self.f(med) * self.f(b) < 0:  # Добавлено elif для повышения эффективности
                a = med
        return float((a + b) / 2)
    
    def calculate_std_deviation(self, found_root):
        if self.true_root is None:
            raise ValueError("Истинный корень не задан.")
        deviation = abs(found_root - self.true_root)
        return np.std([deviation])
    
    def graph (self, mid_point, intervals):
        mid_x = mid_point
        mid_y = [self.f(x) for x in mid_x]
        n = 1000
        x_vals = [x / n for x in range(int(self.a * n), int(self.b * n))]  # Точки от a до b
        y_vals = [self.f(x) for x in x_vals]

        plt.figure(figsize=(14, 6))

        plt.subplot(1, 2, 1)
        plt.plot(x_vals, y_vals, label = 'Функция f(x)', color = "blue")
        plt.scatter(mid_x, mid_y, label = 'Точки экстремума', color = "red")
        plt.title("Положение точек экстремума")
        plt.xlabel("X")
        plt.ylabel("f(x)")
        plt.grid()
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(range(len(intervals)), intervals, marker="o", linestyle="-", label="Длина интервала")
        plt.title("Изменение длины интервала неопределённости")
        plt.xlabel("Итерация")
        plt.ylabel("Длина интервала")
        plt.grid()
        plt.legend()

        plt.tight_layout()
        plt.show()

class FunctionError(Exception):
    def __init__(self, message):
        super().__init__(message)

# user_func = str(input("Введите свою функцию (например 'x**4 - 5'): "))
# func = Function(user_func)
# a, b = map(float, input("Введите левую и правую границы: ").split())
# epsilon = float(input("Введите точность для Epsilon (например 1e-6): "))

user_func = 'x**3 - 6*x**2 + 11*x - 6'
a, b, epsilon = 0, 4, 1e-6
true_root = 2
func = Function(user_func, a, b, epsilon, true_root=true_root)

# func_minimum = func.alg_dihotomia()
# func_minimum = func.alg_golden_ratio()

# print(f"Минимум функции на отрезке [{a}, {b}] приблизительно равен: {func_minimum}")
# target = float(input("Введите для какого значения функции надо найти корень: "))

root = func.root()
print(f"Корень функции на отрезке [{a}, {b}] приблизительно равен: {root}")

# Рассчитать СКО
std_dev = func.calculate_std_deviation(root)
print(f"Среднеквадратичное отклонение: {std_dev}")