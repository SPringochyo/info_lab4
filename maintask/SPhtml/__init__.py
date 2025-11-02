class HTML:

    def __init__(self, filename: str = "") -> None:
        self.FILE_NAME = filename
        self.MAIN_STRING = self._convert_to_string()


    def _convert_to_string(self) -> str:
        file = open(self.FILE_NAME, "r")
        string = [s.strip() for s in file.readlines()]
        template_string = ''.join(string)

        return template_string


    def _split_the_string(self, string : str) -> list[str]:

        strings = []

        while string:

            open_tag = ""

            if string[0] == '<':
                for i in range(len(string)):
                    if string[i] == '>':
                        open_tag = string[: i+1]
                        break

                tag_data = open_tag[1:-1].split()
                tag_name = tag_data[0]
                index_of_open_tag_end = i + 1

                tmp_string = string[index_of_open_tag_end:]
                length_of_close_tag = len(tag_name) + 2

                index_after_close_tag = self._find_tag_closure(tmp_string, length_of_close_tag, tag_name)

                strings.append(string[:index_of_open_tag_end + index_after_close_tag + length_of_close_tag + 1])

                string = string[index_of_open_tag_end + index_after_close_tag + length_of_close_tag + 1:]

            else:
                if "</" in string:
                    strings.append(string[:string.find("<")])
                    string = string[string.find("<"):]
                else:
                    strings.append(string)
                    string = ""

        return strings


    def _find_tag_closure(self, string : str, length_of_close_tag : int, tag_name : str) -> int:

        flag = 1

        for i in range(len(string) - length_of_close_tag):
            sub_string = string[i:i+length_of_close_tag+1]

            if sub_string[:-2] == ("<" + tag_name):
                flag += 1
            elif sub_string == ("</" + tag_name + ">"):
                flag -= 1

            if flag == 0:
                break

        index_of_tag_closure = i

        return index_of_tag_closure


    def _find_tag_opening(self, string : str) -> list:

        open_tag = ""
        basic_tag_info = []

        if string:
            if string[0] == '<':
                for i in range(len(string)):
                    if string[i] == '>':
                        open_tag = string[: i+1]
                        break

        index_of_end_open_tag = i + 1

        tag_data = open_tag[1:-1].split()

        basic_tag_info.append(index_of_end_open_tag)
        basic_tag_info.append(dict())

        basic_tag_info[1]["TAG_NAME"] = tag_data[0]
        basic_tag_info[1]["TAG_ATTRS"] = dict()

        for attr in tag_data[1:]:
            basic_tag_info[1]["TAG_ATTRS"][attr[:attr.find("=")]] = attr[attr.find("=")+2:-1]

        return basic_tag_info


    def _parse_tag_info(self, string : str) -> dict:    # dict/str

        if "</" not in string: return string

        open_tag = self._find_tag_opening(string)

        tag_name = open_tag[1]["TAG_NAME"]

        string = string[open_tag[0]:]
        length_of_close_tag = len(tag_name) + 2
        index_after_close_tag = self._find_tag_closure(string, length_of_close_tag, tag_name)
        content = string[:index_after_close_tag]

        open_tag[1]["CONTENT"] = self._dump(content)

        return open_tag[1]


    def _dump(self, string : str) -> list[dict, str]:
        list_of_tags = []

        for sub_string in self._split_the_string(string):
            list_of_tags.append(self._parse_tag_info(sub_string))

        return list_of_tags


    def parse(self) -> list[dict]:
        root_list_of_tags = []

        string = self.MAIN_STRING[:]

        for sub_string in self._split_the_string(string):
            root_list_of_tags.append(self._parse_tag_info(sub_string))

        return root_list_of_tags
