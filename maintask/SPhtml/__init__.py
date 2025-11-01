# tag-open := '<' tag-name ws* attr-list? ws* '>'
# tag-empty := '<' tag-name ws* attr-list? ws* '/>'
# tag-close := '</' tag-name ws* '>'

# attr-list := (ws+ attr)*
# attr := attr-empty | attr-unquoted | attr-single-quoted | attr-double-quoted

# attr-empty := attr-name
# attr-unquoted := attr-name ws* = ws* attr-unquoted-value
# attr-single-quoted := attr-name ws* = ws* ' attr-single-quoted-value '
# attr-double-quoted := attr-name ws* = ws* " attr-double-quoted-value "

# tag-name := (alphabets | digits)+                      # Can digits become first letter?
# attr-name := /[^\s"'>/=\p{Control}]+/

# # These three items should not contain 'ambiguous ampersand'...
# attr-unquoted-value := /[^\s"'=<>`]+/
# attr-single-quoted-value := /[^']*/
# attr-double-quoted-value := /[^"]*/

# alphabets := /[a-zA-Z]/
# digits := /[0-9]/
# ws := /\s/

WHITESPACES = [" ", "\t", "\b", "\n", "\r"]


class HTML:

    # FILE_NAME = ""
    # MAIN_STR = ""
    indexofsearch = 0


    def __init__(self, filename: str) -> None:
        self.FILE_NAME = filename
        self.MAIN_STR = self._to_string()


    def _to_string(self) -> str:
        file = open(self.FILE_NAME, "r")
        string = [s.strip() for s in file.readlines()]
        rez = ''.join(string)

        return rez


    def _tag_open(self, string : str) -> list:

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
        rez.append(tagdata[0])
        rez.append(tagdata[1:])

        return rez

    #                                                        ПЕРЕПИСАТЬ!!!
    def _tag_close(self, string : str) -> list:
    
        opentag = self._tag_open(string)
        closetag = ""
        content = ""
        rez = opentag
        flag = 1

        if ("<" + opentag[1]) in string[:]:
            if string[:].find("<" + opentag[1]) < string[:].find("</" + opentag[1] + ">"):
                tmp = []
                for i in string[:].split("<" + opentag[1]):
                    if ("</" + opentag[1] + ">") in i:
                        tmp2 = i.split("</" + opentag[1] + ">")
                        for j in tmp2:
                            tmp.append(j)
                            tmp.append("</" + opentag[1] + ">")
                    else:
                        tmp.append(i)
                    tmp.append("<" + opentag[1])
                del tmp[-1]

                ln = 0

                for i in tmp:
                    if i == ("<" + opentag[1] + ">"):
                        flag += 1
                    elif i == ("</" + opentag[1] + ">"):
                        flag -= 1

                    if flag == 0:
                        n = ln + 0
                        break
                    else:
                        ln += len(i)

            else:
                n = string.find("</" + opentag[1] + ">")
        else:
            n = string.find("</" + opentag[1] + ">")

        if string[n:]:
            for i in range(len(string[n:])):
                if string[n:][i] == '>':
                    closetag = string[n:][: i+1]
                    break

        content = string[opentag[0] : n]

        rez.append(content)
        self.indexofsearch += (n + len(closetag))

        return rez[1:]


    def _parse(self) -> list:
        string = self.MAIN_STR[self.indexofsearch:]
        return self._tag_close(string)


    def dump(self) -> dict:

        rez = {}

        while self.MAIN_STR[self.indexofsearch:]:
            tmp = self._parse()
            rez[tmp[0]] = tmp[1:]

        return rez
