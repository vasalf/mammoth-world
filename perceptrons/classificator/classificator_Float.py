#!/usr/bin/python3

from Float import Float


class perceptron:
    def __init__(self, n):
        self.__n = n
        self.__edges = dict()
        
        # 1-weight edges
        for i in range(n):
            self.__edges[(2 * i, 2 * n + i)] = Float(1)

        # v-weight edges
        for i in range(n):
            self.__edges[(2 * i + 1, 2 * n + i)] = Float(1)

        # lambda-weight edges
        for i in range(n):
            self.__edges[(2 * n + i, 3 * n)] = Float(1)

    def get_val(self, arr):
        n = self.__n
        a_neurons_vals = [Float() for i in range(self.__n)]
        for i in range(self.__n):
            a_neurons_vals[i] += arr[i] * self.__edges[(2 * i, 2 * n + i)]
            a_neurons_vals[i] += (-1) * self.__edges[(2 * i + 1, 2 * n + i)]
        res = Float()
        for i in range(self.__n):
            res += a_neurons_vals[i] * self.__edges[(2 * n + i, 3 * n)]
        return 1 if res > 0 else -1

    def insert_val(self, arr, ans):
        n = self.__n
        zeta = self.get_val(arr)
        if zeta == ans:
            return
        else:
            for i in range(n):
                x = ans * Float(arr[i])
                self.__edges[(2 * n + i, 3 * n)] += x
                lambdas = self.__edges[(2 * n + i, 3 * n)]
                v = self.__edges[(2 * i + 1, 2 * n + i)]
                if zeta > 0:
                    v = v + (v * x + v * v) / lambdas
                else:
                    v = v + (v * x - v * v) / lambdas
                self.__edges[(2 * i + 1, 2 * n + i)] = v

    def print_plane(self):
        n = self.__n
        coef = [0 for i in range(4)]
        for i in range(3):
            coef[i] += self.__edges[(2 * n + i, 3 * n)]
            coef[-1] += self.__edges[(2 * n + i, 3 * n)] * self.__edges[(2 * i + 1, 2 * n + i)]
        print(coef)
        for i in range(3):
            print("lambda", i, self.__edges[(2 * n + i, 3 * n)])
            print("v", i, self.__edges[(2 * i + 1, 2 * n + i)])


from random import randint


def test(k):
    hyperplane = [randint(-10, 10) for i in range(k + 1)]
    print(hyperplane)
    NUM = 10 ** 4
    p = perceptron(k)
    for i in range(100 * NUM):
        val = [randint(-100, 100) for i in range(k)]
        res = hyperplane[-1]
        for i in range(k):
            res += val[i] * hyperplane[i]
        res = 1 if res > 0 else -1
        p.insert_val(val, res)
    num = 0
    print("Finished education")
    for i in range(NUM):
        val = [randint(-100, 100) for i in range(k)]
        res = hyperplane[-1]
        for i in range(k):
            res += val[i] * hyperplane[i]
        res = 1 if res > 0 else -1
        zeta = p.get_val(val)
        if zeta != res:
            num += 1
#    p.print_plane()
    print("perceptron has %d mistakes in %d questions (%.02f)" % (num, NUM, num / NUM))
    return num / NUM



test(int(input()))
