import colored

d = dict()
d['W'] = ['W', '', 'red', 0, 'red', 0, []]
d['B'] = ['B', '', 'green', 0, 'dark_blue', 0, ['blinked']]
d['\n'] = [' ', '\n', 'gray', 0, 'gray', 0, []]
fin = open('02')
fin.readline()
a = fin.read().rstrip('\n2')

for c in a:
#    print(c, end = '')
    colored.colored_print(*d[c])
