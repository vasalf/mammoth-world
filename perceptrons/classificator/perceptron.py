#!/usr/bin/pypy3

class perceptron:
    def __init__(self, s, r):
        self.__has_examples = False
        self.__s = s
        self.__r = r
        
        self.__sr_edges = dict()
        for s_el in range(s):
            for r_el in range(r):
                self.__sr_edges[(s_el, r_el)] = 0
        

    def __get_val(self, s_val):
        # R-elements values
        r_val = [0 for i in range(self.__r)]
        for r in range(self.__r):
            for s in range(self.__s):
                r_val[r] += s_val[s] * self.__sr_edges[(s, r)]
        return r_val

    def __norm(self, vect):
        return[(1 if vect[i] > 0 else -1) for i in range(len(vect))]

    def get_val(self, s_arr):
        return self.__norm(self.__get_val(s_arr))

    def insert_ans(self, s_val, r_val):
        if not self.__has_examples:
            for r in range(self.__r):
                for s in range(self.__s):
                    self.__sr_edges[(s, r)] = r_val[r] * s_val[s]
            self.__has_examples = True
        else:
            our_res = self.get_val(s_val)
            for r in range(self.__r):
                if our_res[r] != r_val[r]:
                    for s in range(self.__s):
                        self.__sr_edges[(s, r)] += r_val[r] * s_val[s]
    
    def print_vec(self):
        for s in range(self.__s):
            for r in range(self.__r):
                print(str(self.__sr_edges[(s, r)]).ljust(5), end=" ")
            print()


from random import randint

def test(k):
    p = perceptron(k, k)
    
    NUM = 100000
    for i in range(100 * NUM):
        s = [randint(-100, 100) for j in range(k)]
        r = [(1 if s[j] > 0 else -1) for j in range(k)]
        p.insert_ans(s, r)

    p.print_vec()
    print("Finished education")

    cnt = 0
    for i in range(NUM):
        s = [randint(-100, 100) for j in range(k)]
        r = [(1 if s[j] > 0 else -1) for j in range(k)]
        if r != p.get_val(s):
            cnt += 1

    print("perceptron has %d mistakes in %d questions (%.02f)" % (cnt, NUM, cnt / NUM))

test(int(input()))
 
