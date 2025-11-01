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


    def _cutstr(self, string : str) -> list:

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

                beforeclosetag = self._tagclosefind(tmpstr, ln, tagname)

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


    def _tagclosefind(self, string : str, ln : int, tagname : str) -> int:

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
        rez.append(dict())

        rez[1]["tagname"] = tagdata[0]
        rez[1]["tagattrs"] = tagdata[1:]

        return rez

    def _tag_close(self, string : str) -> dict:
        if "</" not in string:
            return string

        opentag = self._tag_open(string)
        tagname = opentag[1]["tagname"]

        string = string[opentag[0]:]
        ln = len(tagname) + 2

        i = self._tagclosefind(string, ln, tagname)

        content = string[:i]

        opentag[1]["content"] = self._parse(content)
        return opentag[1]


    def _parse(self, string : str) -> list:
        rez = []

        for str in self._cutstr(string):
            rez.append(self._tag_close(str))

        return rez

    def parse(self) -> list:
        rez = []

        string = self.MAIN_STR

        for str in self._cutstr(string):
            rez.append(self._tag_close(str))

        return rez
