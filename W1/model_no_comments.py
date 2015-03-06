import random
import time
import sys

class queue:
    def __init__(self):
        self.arr = []
        self.b = 0
        self.e = 0
    def put(self, elem):
        self.arr.append(elem)
        self.e += 1
    def get(self):
        return self.arr[b]
    def pop(self):
        b += 1
        return self.arr[b - 1]

sys.setrecursionlimit(1000000)
def foo(starti, startj):
    #global taken
    #if taken != s_to_take:
        #if starti != 0 and A[starti - 1][startj] == enemy and taken != s_to_take:
            #A[starti - 1][startj] = country
            #taken += 1
            #foo(starti - 1, startj)
        #if starti != n - 1 and A[starti + 1][startj] == enemy and taken != s_to_take:
            #A[starti + 1][startj] = country
            #taken += 1
            #foo(starti + 1, startj)
        #if startj != 0 and A[starti][startj - 1] == enemy and taken != s_to_take:
            #A[starti][startj - 1] = country
            #taken += 1
            #foo(starti, startj - 1)
        #if startj != n - 1 and A[starti][startj + 1] == enemy and taken != s_to_take:
            #A[starti][startj + 1] = country
            #taken += 1
            #foo(starti, startj + 1)
    q = queue()
    q.put((starti, startj))
    while q and taken < s_to_take:
        starti, startj = q.get()
        if starti != 0 and A[starti - 1][startj] == enemy:
            taken += 1
            A[starti - 1][startj] = country
            q.put((starti - 1, startj))

n = 720
years = 2700
size = 20
fout = open("results_of_model.txt", "w")
time.clock()
A = [[0] * (n) for i in range(n)]
for i in range(n):
    for j in range(n):
        if i % size == 0:
            A[i][j] = int(j // size + i // size * n // size + 1)
        else:
            A[i][j] = A[i - 1][j]
#for row in A:
    #print(" ".join(map(lambda x: str(x).rjust(3), row)))
Countries = [i + 1 for i in range(n // size * (n // size))]
S_countries = dict()
for country in Countries:
    S_countries[country] = size * size
last_available = n // size * (n // size) + 1
wars = 0
divisions = 0
ruined = 0
New_Countries = []
Ruined_Countries = []
for k in range(1, years + 1):
    country = random.choice(Countries)
    event = random.choice([False, False, True, True, True])
    s = S_countries[country]
    if not event and s > 4:                                            
        divisions += 1
        div_part = random.randrange(1, s)
        div = 0
        how_divide = random.randrange(8)
        if how_divide == 0:
            i = 0
            while i < n and div != div_part:
                j = 0
                while j < n and div != div_part:
                    if A[i][j] == country:
                        A[i][j] = last_available
                        div += 1
                    j += 1
                i += 1
        elif how_divide == 1:
            i = 0
            while i < n and div != div_part:
                j = n - 1
                while j >= 0 and div != div_part:
                    if A[i][j] == country:
                        A[i][j] = last_available
                        div += 1
                    j -= 1
                i += 1
        elif how_divide == 2:
            i = n - 1
            while i >= 0 and div != div_part:
                j = 0
                while j < n and div != div_part:
                    if A[i][j] == country:
                        A[i][j] = last_available
                        div += 1
                    j += 1
                i -= 1
        elif how_divide == 3:
            i = n - 1
            while i >= 0 and div != div_part:
                j = n - 1
                while j >= 0 and div != div_part:
                    if A[i][j] == country:
                        A[i][j] = last_available
                        div += 1
                    j -= 1
                i -= 1               
        elif how_divide == 4:
            j = 0
            while j < n and div != div_part:
                i = 0
                while i < n and div != div_part:
                    if A[i][j] == country:
                        A[i][j] = last_available
                        div += 1
                    i += 1
                j += 1
        elif how_divide == 5:
            j = 0
            while j < n and div != div_part:
                i = n - 1
                while i >= 0 and div != div_part:
                    if A[i][j] == country:
                        A[i][j] = last_available
                        div += 1
                    i -= 1
                j += 1
        elif how_divide == 6:
            j = n - 1
            while j >= 0 and div != div_part:
                i = 0
                while i < n and div != div_part:
                    if A[i][j] == country:
                        A[i][j] = last_available
                        div += 1
                    i += 1
                j -= 1
        else:
            j = n - 1
            while j >= 0 and div != div_part:
                i = n - 1
                while i >= 0 and div != div_part:
                    if A[i][j] == country:
                        A[i][j] = last_available
                        div += 1
                    i -= 1
                j -= 1               
        Countries.append(last_available)
        S_countries[country] -= div_part
        S_countries[last_available] = div_part
        last_available += 1
        #New_Countries.append(last_available)
        print("In the year ", k, " Country ", country, " successfully divided in Country ", country, " and Country ", last_available - 1, " with proporsion ", s - div_part, " : ", div_part, ".", sep = "")
    else: #
        wars += 1
        Possible_vars = set()
        Touches = dict()
        Free = 0
        for i in range(n):   # 
            for j in range(n):
                if A[i][j] == country:
                    if i != 0:
                        Possible_vars.add(A[i - 1][j])
                        Touches[A[i - 1][j]] = (i, j)
                    if i != n - 1:
                        Possible_vars.add(A[i + 1][j])
                        Touches[A[i + 1][j]] = (i, j)
                    if j != 0:
                        Possible_vars.add(A[i][j - 1])
                        Touches[A[i][j - 1]] = (i, j)
                    if j != n - 1:
                        Possible_vars.add(A[i][j + 1])
                        Touches[A[i][j + 1]] = (i, j)
        if country in Possible_vars:
            Possible_vars.remove(country)
        if not Possible_vars:
            print("In the year", k, "Country", country, "won everyone!", Possible_vars, Touches, country in Countries)
            break
        peace = False
        if 0 in Possible_vars:
            peace = random.choice([False, False, True, True, True])
        if not Free or not peace:  #
            enemy = random.choice(list(Possible_vars))           
            s_enemy = S_countries[enemy]
            all_take = random.choice([True, True, False, False, False])
            if all_take or s_enemy == 1:
                s_to_take = s_enemy
            else:
                s_to_take = random.randrange(1, s_enemy)
            taken = 0
            foo(Touches[enemy][0], Touches[enemy][1])
            S_countries[country] += taken
            S_countries[enemy] -= taken
            if S_countries[enemy] == 0:
                ruined += 1
                Countries.pop(Countries.index(enemy))    
                print("In the year ", k, " Country ", enemy, " was taken by Country ", country, ".", sep = "")             
            else:               
                print("In the year ", k, " ", "part of Country ", enemy, " was taken by ", country, ".", sep = "")
        else:
            s_to_take = random.randrange(1, s // 2)
            taken = 0
            foo(country, Free[0], Free[1], A, n, s_to_take, taken)
        #Possible_vars = set()
        #Touches = dict()
        #s = 0
        #s_to_take = 0
    #for row in A:
        #print(" ".join(map(lambda x: str(x).rjust(3), row)))
    
time_ex = time.clock()
fout = open("results_of_model.txt", "w")
print("Side of continent was ", n, ", side of country was ", size, ", so size of country was ", size * size, ", so there were ", (n // size) ** 2, " countries. ", years, " years passed.", file=fout, sep = "")
print("As a result we had:", file=fout)
print(divisions, "divisions, in which appeared many new countries.", file=fout)
print("However, we had", wars, "wars, in which", ruined, "countries were destroyed.", file=fout)
Numbers = [0] * 9
for country in Countries:
    Numbers[int(str(S_countries[country])[0]) - 1] += 1
print("And, probably, the most important thing:", file=fout)
for i in range(9):
    print(i + 1, Numbers[i], round(Numbers[i] / len(Countries) * 100, 2), "%", file=fout)
print("Execution time:", time_ex, "seconds or", time_ex / 60, "minutes.", file=fout)
print(len(Countries), "countries remained.", file=fout)
To_Print = []
for country in S_countries:
    if S_countries[country] != 0:
        To_Print.append(S_countries[country])
print(" ".join(map(str, sorted(To_Print))), file=fout)
#for i in range(n):
    #for j in range(n):
        #print(str(A[i][j]).rjust(4), end = " ", file=fout)
    #print(file=fout)
fout.close()
