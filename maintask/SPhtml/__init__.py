class HTML:

    def __init__(self, filename: str) -> None:
        self.FILE_NAME = filename
        self.MAIN_STRING = self._convert_to_string()


    def _convert_to_string(self) -> str:
        file = open(self.FILE_NAME, "r")
        string = [s.strip() for s in file.readlines()]
        templatestring = ''.join(string)

        return templatestring


    def _split_the_string(self, string : str) -> list[str]:

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
                indexofopentagend = i + 1

                tmpstr = string[indexofopentagend:]
                lengthofclosetag = len(tagname) + 2

                indexbeforeclosetag = self._find_tag_closure(tmpstr, lengthofclosetag, tagname)

                strings.append(string[:indexofopentagend + indexbeforeclosetag + lengthofclosetag + 1])

                string = string[indexofopentagend + indexbeforeclosetag + lengthofclosetag + 1:]

            else:
                if "</" in string:
                    strings.append(string[:string.find("<")])
                    string = string[string.find("<"):]
                else:
                    strings.append(string)
                    string = ""

        return strings


    def _find_tag_closure(self, string : str, lengthofclosetag : int, tagname : str) -> int:

        flag = 1

        for i in range(len(string) - lengthofclosetag):
            substring = string[i:i+lengthofclosetag+1]

            if substring[:-2] == ("<" + tagname):
                flag += 1
            elif substring == ("</" + tagname + ">"):
                flag -= 1

            if flag == 0:
                break

        indexoftagclosure = i

        return indexoftagclosure


    def _find_tag_opening(self, string : str) -> list:

        opentag = ""
        basictaginfo = []

        if string:
            if string[0] == '<':
                for i in range(len(string)):
                    if string[i] == '>':
                        opentag = string[: i+1]
                        break

        indexofendopentag = i + 1

        tagdata = opentag[1:-1].split()

        basictaginfo.append(indexofendopentag)
        basictaginfo.append(dict())

        basictaginfo[1]["TAG_NAME"] = tagdata[0]
        basictaginfo[1]["TAG_ATTRS"] = tagdata[1:]

        return basictaginfo

    def _parse_tag_info(self, string : str) -> dict:    # dict/str

        if "</" not in string: return string

        opentag = self._find_tag_opening(string)

        tagname = opentag[1]["TAG_NAME"]

        string = string[opentag[0]:]
        lengthofclosetag = len(tagname) + 2
        indexbeforeclosetag = self._find_tag_closure(string, lengthofclosetag, tagname)
        content = string[:indexbeforeclosetag]

        opentag[1]["CONTENT"] = self._dump(content)

        return opentag[1]


    def _dump(self, string : str) -> list[dict, str]:
        listoftags = []

        for substring in self._split_the_string(string):
            listoftags.append(self._parse_tag_info(substring))

        return listoftags

    def parse(self) -> list[dict]:
        rootlistoftags = []

        string = self.MAIN_STRING[:]

        for substring in self._split_the_string(string):
            rootlistoftags.append(self._parse_tag_info(substring))

        return rootlistoftags
