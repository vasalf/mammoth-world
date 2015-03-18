#!/usr/bin/pypy3

from perceptron import perceptron


class classificator:
    def __init__(self, s):
        self.__s = s
        
        self.__lambda = perceptron(s, 1)
        self.__v = perceptron(s, 1)

    def __get_v(self):
        k = self.__v.get_dict()
        res = [k[(i, 0)] for i in range(self.__s)]
        return res

    def __get_lambda(self):
        k = self.__lambda.get_dict()
        res = [k[(i, 0)] for i in range(self.__s)]
        return res

    def get_val(self, p):
        v = self.__get_v()
        np = [p[i] - v[i] for i in range(self.__s)]
        return self.__lambda.get_val(np)[0]

    def insert_ans(self, p, ans):
        v = self.__get_v()
        np = [p[i] - v[i] for i in range(self.__s)]
        self.__lambda.insert_ans(np, [ans])
        Lambda = self.__get_lambda()
        self.__v.insert_ans(Lambda, [-ans])


from random import randint

def test(k):
    hyperplane = [randint(-100, 100) for i in range(k + 1)]
    print(hyperplane)
    NUM = 100000
    p = classificator(k)
    for i in range(100 * NUM):
        pt = [randint(-100, 100) for i in range(k)]
        val = hyperplane[k]
        for i in range(k):
            val += hyperplane[i] * pt[i]
        if val > 0:
            ans = 1
        else:
            ans = -1
        p.insert_ans(pt, ans)
    print("Classificator educated")
    mistakes = 0
    y = 0
    no = 0
    for i in range(NUM):
        pt = [randint(-100, 100) for i in range(k)]
        val = hyperplane[k]
        for i in range(k):
            val += hyperplane[i] * pt[i]
        if val > 0:
            ans = 1
        else:
            ans = -1
        n = p.get_val(pt)
        if ans != n:
            mistakes += 1
        if n == 1:
            y += 1
        else:
            no += 1
    print("classificator has %d mistakes in %d questions (%.02f)" % (mistakes, NUM, mistakes / NUM))
    print("classificator gave %d positive answers and %d negative answers" % (y, no))


test(int(input()))

