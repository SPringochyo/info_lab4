# t = "abcdef"

# m = 5

# for i in range(len(t) - m):
#     print(t[i:i+m+1])

from maintask.SPhtml import *

T = HTML("test.html")

MSTR = T.MAIN_STR

def tag_open(string : str) -> list:

    opentag = ""
    rez = []

    if string:
        if string[0] == '<':
            for i in range(len(string)):
                if string[i] == '>':
                    opentag = string[: i+1]
                    break

    tagdata = opentag[1:-1].split()

    rez.append(i + 1)

    rez.append(dict())

    rez[1]["tagname"] = tagdata[0]
    rez[1]["tagattrs"] = tagdata[1:]

    return rez

def tag_close(string : str) -> list:
    opentag = tag_open(string)
    tagname = opentag[1]["tagname"]
    flag = 1

    string = string[opentag[0]:]
    ln = len(tagname) + 2

    for i in range(len(string) - ln):
        str = string[i:i+ln+1]

        if str[:-2] == ("<" + tagname):
            flag += 1
        elif str == ("</" + tagname + ">"):
            flag -= 1

        if flag == 0:
            break

    content = string[:i]

    if "</" not in content:
        opentag[1]["content"] = content
        return opentag[1]

    else:
        opentag[1]["innertag"] = tag_close(content)
        return opentag[1]

print(tag_close(MSTR))
