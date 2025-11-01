def cutstr(string : str) -> list:

    strings = []

    while string:

        opentag = ""

        if string[0] == '<':
            for i in range(len(string)):
                if string[i] == '>':
                    opentag = string[: i+1]
                    break

            tagdata = opentag[1:-1].split()
            tagname = tagdata[0]
            opentagend = i + 1

            tmpstr = string[opentagend:]
            ln = len(tagname) + 2

            beforeclosetag = tagclosefind(tmpstr, ln, tagname)

            strings.append(string[:opentagend + beforeclosetag + ln + 1])

            string = string[opentagend + beforeclosetag + ln + 1:]

        else:
            if "</" in string:
                strings.append(string[:string.find("<")])
                string = string[string.find("<"):]
            else:
                strings.append(string)
                string = ""

    return strings


def tagclosefind(string : str, ln : int, tagname : str) -> int:

    flag = 1

    for i in range(len(string) - ln):
        str = string[i:i+ln+1]

        if str[:-2] == ("<" + tagname):
            flag += 1
        elif str == ("</" + tagname + ">"):
            flag -= 1

        if flag == 0:
            break

    return i


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

def tag_close(string : str) -> dict:
    if "</" not in string:
        return string

    opentag = tag_open(string)
    tagname = opentag[1]["tagname"]

    string = string[opentag[0]:]
    ln = len(tagname) + 2

    i = tagclosefind(string, ln, tagname)

    content = string[:i]

    opentag[1]["content"] = parse(content)
    return opentag[1]


def parse(string : str) -> list:
    rez = []

    for str in cutstr(string):
        rez.append(tag_close(str))

    return rez


from maintask.SPhtml import *

T = HTML("index.html")

MSTR = T.MAIN_STR

print(parse(MSTR))
