##constants
__colors__ = {}
__colors__["black"] = 30
__colors__["red"] = 31
__colors__["green"] = 32
__colors__["yellow"] = 33
__colors__["dark_blue"] = 34
__colors__["purpur"] = 35
__colors__["light_blue"] = 36
__colors__["gray"] = 37
__specials__ = {}
__specials__["inverse"] = 7
__specials__["hard"] = 1
__specials__["light"] = 2
__specials__["underlined"] = 4
__specials__["hidden"] = 8
__specials__["blinked"] = 5
def colored_print(string, end='', color="black", version=0, bg = "gray", version_back= 0, special = []):
    res = ["\033["]
    col = ""
    for c in special:
        col += str(__specials__[c]) + ';'
    col += str(__colors__[color] + 60 * version) + ';'
    col += str(10 + __colors__[bg] + 60 * version)
    res.append(col)
    res.append('m')
    res.append(string)
    res.append("\033[0m")
    print(''.join(res), end=end)

def Help():
    print("""
    colors = [""" + ', '.join(list(__colors__.keys())) + """], 
    special = [""" + ', '.join(list(__specials__.keys())) + """],
    example:
        colored_print("abacaba", end="", color="green",
        version=0, bg="red", version_back=0, special = ["blinked", "inverse"])""")
#colored_print("abacaba", end="\n", color="green", version=1, bg="yellow", version_back=1, special = ["blinked", "inverse"])
Help()
