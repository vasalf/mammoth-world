#!/usr/bin/python3


class segment_tree:
    def __build(self, v, L, R):
        if L == R - 1:
            self.__tree[v] = self.__arr[L]
        else:
            mid = (L + R) // 2
            self.__build(2 * v + 1, L, mid)
            self.__build(2 * v + 2, mid, R)
            self.__tree[v] = min(self.__tree[2 * v + 1],
                self.__tree[2 * v + 2])

    def __get_val(self, v, L, R, i):
        if i < L or R <= i:
            return False
        elif L == R - 1:
            return self.__tree[v] != self.__inf
        else:
            mid = (L + R) // 2
            return self.__get_val(2 * v + 1, L, mid, i) or \
                self.__get_val(2 * v + 2, mid, R, i)

    def __update(self, v, L, R, i, val):
        if i < L or R <= i:
            return
        elif L == R - 1:
            self.__tree[v] = val
        else:
            mid = (L + R) // 2
            self.__update(2 * v + 1, L, mid, i, val)
            self.__update(2 * v + 2, mid, R, i, val)
            self.__tree[v] = min(self.__tree[2 * v + 1],
                self.__tree[2 * v + 2])

    def __init__(self, n, arr, inf):
        self.__arr = sorted(arr)[:]
        self.__tree = [0] * (4 * n)
        self.__inf = inf
        self.__build(0, 0, n)
        self.__size = n

    def __getindex(self, item):
        l, r = -1, self.__size
        while l < r - 1:
            mid = (l + r) // 2
            if self.__arr[mid] < item:
                l = mid
            else:
                r = mid
        return r

    def __getitem__(self, item):
        i = self.__getindex(item)
        if i == self.__size or self.__arr[i] != item:
            return False
        return self.__get_val(0, 0, self.__size, i)

    def remove(self, item):
        i = self.__getindex(item)
        self.__update(0, 0, self.__size, i, self.__inf)

    def get_min(self):
        return self.__tree[0]

    def get_tree(self):
        return self.__tree


def get_mountain_array(point_array):
    point_st = set()
    for x, y in point_array:
        point_st.add((x, y))
        point_st.add((x, y + 1))
        point_st.add((x + 1, y))
        point_st.add((x + 1, y + 1))
    d = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    inf = 1791791791, 1791791791
    st = segment_tree(len(point_st), point_st, inf)
    res = []
    while st.get_min() != inf:
        cur = st.get_min()
        gen = True
        st.remove(cur)
        res.append([cur])
        while gen:
            gen = False
            for dx, dy in d:
                if not gen and st[cur[0] + dx, cur[1] + dy]:
                    cur = cur[0] + dx, cur[1] + dy
                    gen = True
            if gen:
                st.remove(cur)
                res[-1].append(cur)
    return res


n = int(input())
arr = [tuple(map(int, input().split())) for i in range(n)]
print("\n".join(map(str, get_mountain_array(arr))))

